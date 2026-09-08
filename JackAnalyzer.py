import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def main():
    """
    Main function to drive the Jack Compiler.
    """
    if len(sys.argv) != 2:
        print("Usage: python Main.py <file_or_directory.jack>")
        return

    input_path = sys.argv[1]
    jack_files = []

    if os.path.isfile(input_path) and input_path.endswith('.jack'):
        jack_files.append(input_path)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith('.jack'):
                jack_files.append(os.path.join(input_path, filename))
    else:
        print(f"Error: Invalid input. Please provide a .jack file or a directory containing .jack files.")
        return

    for jack_file in jack_files:
        print(f"Compiling {jack_file}...")
        
        output_file_path = jack_file.replace('.jack', '.xml')
        
        try:
            tokenizer = JackTokenizer(jack_file)
            compiler = CompilationEngine(tokenizer, output_file_path)
            
            compiler.compile_class()
            
            print(f"Successfully created {output_file_path}")
            
        except Exception as e:
            print(f"An error occurred while compiling {jack_file}: {e}")

if __name__ == '__main__':
    main()