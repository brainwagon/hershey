from typing import cast, Dict, List, Optional, Tuple

def parse_hershey_font(filename: str) -> Dict[int, Dict[str, object]]:
    """
    Parse a Hershey font file and return a dictionary of glyph definitions.

    Args:
        filename (str): Path to the Hershey font file

    Returns:
        dict: Dictionary where keys are glyph numbers and values are dictionaries containing:
            - 'left': left hand position
            - 'right': right hand position
            - 'coordinates': list of (x, y) tuples with None indicating pen up operations
    """
    glyphs: Dict[int, Dict[str, object]] = {}

    with open(filename, 'r') as file:
        lines: List[str] = [line.rstrip('\n\r') for line in file]  # Read all lines and remove line endings

    i: int = 0
    while i < len(lines):
        line: str = lines[i]

        if len(line) < 10:  # Skip lines that are too short
            i += 1
            continue

        try:
            # Parse glyph number (columns 0:4, right-justified)
            glyph_num: int = int(line[0:5].strip())

            # Parse number of vertices (columns 5:7)
            num_vertices: int = int(line[5:8])

            # Parse left and right positions (columns 8 and 9)
            left_char: str = line[8]
            right_char: str = line[9]
            left_pos: int = ord(left_char) - ord('R')
            right_pos: int = ord(right_char) - ord('R')

            # Collect all coordinate data, potentially from multiple lines
            coord_data: str = line[10:]  # Start with data from first line

            # The number of coordinate pairs we need (num_vertices includes left/right positions)
            target_pairs: int = num_vertices - 1

            line_idx: int = i
            # Continue reading lines until we have enough character pairs for all coordinates
            while len(coord_data) < target_pairs * 2 and line_idx + 1 < len(lines):
                line_idx += 1
                # Continuation lines contain only coordinate data (no header)
                coord_data += lines[line_idx]

            # Debug output for troubleshooting
            # print(f"Glyph {glyph_num}: target_pairs={target_pairs}, coord_data_len={len(coord_data)}, coord_data='{coord_data}'")

            # Now process all the coordinate data
            coordinates: List[Optional[Tuple[int, int]]] = []
            j: int = 0

            # Process exactly target_pairs coordinate pairs
            while j < len(coord_data) - 1 and len(coordinates) < target_pairs:
                x_char: str = coord_data[j]
                y_char: str = coord_data[j + 1]

                # Check for pen up operation (space followed by 'R')
                if x_char == ' ' and y_char == 'R':
                    coordinates.append(None)
                else:
                    # Convert characters to coordinates relative to 'R'
                    x: int = ord(x_char) - ord('R')
                    y: int = ord(y_char) - ord('R')
                    coordinates.append((x, y))

                j += 2

            # Store the glyph data
            glyphs[glyph_num] = {
                'left': left_pos,
                'right': right_pos,
                'coordinates': coordinates
            }

            # Move to the line after all the data for this glyph
            i = line_idx + 1

        except (ValueError, IndexError) as e:
            # Skip malformed lines
            print(f"Warning: Skipping malformed line: {line[:20]}...")
            i += 1
            continue

    return glyphs



def parse_hershey_mapping(filename: str) -> Dict[str, int]:
    """
    Parse a Hershey font ASCII mapping file and return a dictionary.

    The file contains glyph numbers or ranges separated by whitespace,
    starting from ASCII 32 (space character).

    Args:
        filename (str): Path to the mapping file

    Returns:
        dict: Dictionary where keys are ASCII characters and values are Hershey glyph numbers
    """
    ascii_to_glyph: Dict[str, int] = {}

    with open(filename, 'r') as file:
        content: str = file.read()

    # Split on whitespace to get all tokens
    tokens: List[str] = content.split()

    ascii_code: int = 32  # Start from ASCII 32 (space)

    for token in tokens:
        if '-' in token and not token.startswith('-'):
            # Handle range like "700-709" or "501-526"
            start_str, end_str = token.split('-')
            start_num: int = int(start_str)
            end_num: int = int(end_str)

            # Assign consecutive glyph numbers to consecutive ASCII codes
            for glyph_num in range(start_num, end_num + 1):
                ascii_to_glyph[chr(ascii_code)] = glyph_num
                ascii_code += 1
        else:
            # Handle individual number
            try:
                glyph_num = int(token)
                ascii_to_glyph[chr(ascii_code)] = glyph_num
                ascii_code += 1
            except ValueError:
                # Skip invalid tokens
                print(f"Warning: Skipping invalid token: {token}")
                continue

    return ascii_to_glyph


def print_mapping_info(mapping: Dict[str, int]) -> None:
    """
    Print information about the ASCII to glyph mapping.

    Args:
        mapping (dict): Dictionary from parse_hershey_mapping()
    """
    print(f"Mapping contains {len(mapping)} characters")
    print(f"ASCII range: {ord(min(mapping.keys()))} to {ord(max(mapping.keys()))}")
    print(f"Character range: '{min(mapping.keys())}' to '{max(mapping.keys())}'")

    print("\nFirst 10 mappings:")
    for i, (char, glyph) in enumerate(sorted(mapping.items())[:10]):
        ascii_val: int = ord(char)
        char_display: str = repr(char) if char.isprintable() and char != ' ' else f"ASCII {ascii_val}"
        print(f"  {char_display} -> glyph {glyph}")

    print("\nSample letter mappings:")
    sample_chars: List[str] = ['A', 'B', 'C', 'a', 'b', 'c', '0', '1', '2']
    for char in sample_chars:
        if char in mapping:
            print(f"  '{char}' -> glyph {mapping[char]}")


import ezdxf
import argparse

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to DXF using Hershey fonts.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("text", help="The text to convert to DXF.")
    parser.add_argument("-f", "--font", default="mappings/romant.hmp", help="The Hershey font mapping file to use.")
    parser.add_argument("-o", "--output", default="sign.dxf", help="The name of the output DXF file.")
    parser.add_argument("-d", "--data", default="data/hershey_font.dat", help="The path to the Hershey font data file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output.")
    args = parser.parse_args()

    # Example of how to use the function
    glyphs: Dict[int, Dict[str, object]] = parse_hershey_font(args.data)
    
    # create a DXF 
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    x: int = 0
    y: int = 0
    last: Optional[Tuple[int, int]] = None
    pline: List[Tuple[int, int]] = []
    mapping: Dict[str, int] = parse_hershey_mapping(args.font)
    for ch in args.text:
        if ch in mapping:
            g: int = mapping[ch]
            if g in glyphs:
                if args.verbose:
                    print(f"# glyph {ch} - {g}")
                glyph: Dict[str, object] = glyphs[g]
                left: int = cast(int, glyph["left"])
                right: int = cast(int, glyph["right"])
                coords: List[Optional[Tuple[int, int]]] = cast(List[Optional[Tuple[int, int]]], glyph["coordinates"])
                x = x - left 
                for c in coords:
                    if c == None:
                        if len(pline) > 0:
                            msp.add_lwpolyline(pline)
                        pline = []
                        if args.verbose:
                            print("")
                        last = None
                    else:
                        if args.verbose:
                            print(f"{x+c[0]} {-y-c[1]}")
                        last = (x+c[0], -y-c[1])
                        pline.append(last)
                x += right
        if args.verbose:
            print()
        if len(pline) > 0:
            msp.add_lwpolyline(pline)
        last = None
        pline = []
    doc.saveas(args.output)
