# Password Dictionary Generator

A smart password dictionary generator that creates realistic password combinations using personal information like names, surnames, birth dates, and years. Perfect for security testing and penetration testing scenarios.

## Features

- **Input-Based Generation**: Uses only provided data (names, surnames, years, DOB)
- **Selective Leet Speak**: Strategic character substitutions (a→@, o→0, i→!, s→$, e→3)
- **CamelCase Patterns**: RahulRaval, RavalRahul, RahulRaval@2005
- **Case Variations**: lowercase, Capitalized, UPPERCASE
- **Date Components**: Separate day, month, year combinations
- **Forward & Reverse**: name+surname AND surname+name
- **No Random Data**: Only logical, realistic password patterns

## Installation

```bash
git clone <repository-url>
cd password-dictionary-generator
```

## Usage

### Basic Usage

```bash
python3 dictgen.py --names example/names.txt --surnames example/surnames.txt --years example/years.txt --dob example/dob.txt --output my_wordlist.txt
```

### Parameters

- `--names`: Path to file containing names (one per line)
- `--surnames`: Path to file containing surnames (one per line)  
- `--years`: Path to file containing years (one per line)
- `--dob`: Path to file containing dates in "DD MM YYYY" format
- `--output`: Output wordlist file path
- `--max`: Maximum passwords to generate (default: 100000)

## Input File Formats

### names.txt
```
rahul
priya
aman
```

### surnames.txt
```
raval
shah
```

### years.txt
```
2005
1979
2004
```

### dob.txt
```
12 08 2005
28 01 1977
```

## Example Output

The generator creates realistic password combinations:

```
rahul2005
RahulRaval@2005
r@hul123
priya_shah
pr!ya@123
RavalRahul
admin@123
p@ssw0rd
```

## Generated Password Types

1. **Basic Combinations**
   - rahul2005, priya1979
   - rahul@2005, priya@1979
   - rahul_raval, priya_shah

2. **CamelCase Patterns**
   - RahulRaval, RavalRahul
   - RahulRaval@2005, RavalRahul@1979

3. **Leet Speak Variations**
   - r@hul, pr!ya, p@ssw0rd
   - @dmin, mast3r, adm!n

4. **Date Components**
   - rahul12, priya08 (day/month)
   - rahul197728, priya200508 (combinations)

5. **Common Passwords**
   - admin@123, password, 123456
   - root, master@123, user@123

## Example

See the `example/` folder for sample input files and generated wordlist (21,494 passwords)

## Statistics

With the provided example data:
- **Names**: 3 (rahul, priya, aman)
- **Surnames**: 2 (raval, shah)
- **Years**: 3 (2005, 1979, 2004)
- **DOB entries**: 2 (24 date variants)
- **Generated passwords**: 21,494 unique combinations

## Security Note

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security auditing
- ✅ Password strength assessment
- ✅ Educational purposes

**Always ensure you have proper authorization before using this tool.**

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Author

Created for security testing and educational purposes.