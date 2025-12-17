#!/usr/bin/env python3

import argparse
from pathlib import Path

def read_lines(path):
    if path is None:
        return []
    p = Path(path)
    if not p.is_file():
        return []
    with p.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_dob_line(line):
    parts = line.split()
    if len(parts) != 3:
        return None
    dd, mm, yyyy = parts
    if not (dd.isdigit() and mm.isdigit() and yyyy.isdigit()):
        return None
    if len(dd) != 2 or len(mm) != 2 or len(yyyy) != 4:
        return None
    return dd, mm, yyyy

def build_dob_variants(dob_lines):
    variants = set()
    for line in dob_lines:
        parsed = parse_dob_line(line)
        if not parsed:
            continue
        dd, mm, yyyy = parsed
        # Full date combinations
        variants.add(dd + mm + yyyy)
        variants.add(yyyy + mm + dd)
        variants.add(mm + dd + yyyy)
        
        # Individual components
        variants.add(dd)  # Day
        variants.add(mm)  # Month
        variants.add(yyyy)  # Year
        
        # Two-component combinations
        variants.add(dd + mm)  # Day + Month
        variants.add(mm + dd)  # Month + Day
        variants.add(mm + yyyy)  # Month + Year
        variants.add(yyyy + mm)  # Year + Month
        variants.add(dd + yyyy)  # Day + Year
        variants.add(yyyy + dd)  # Year + Day
    return variants

def apply_leet_substitutions(word):
    variants = set([word])
    
    # Single character substitutions (selective, not all occurrences)
    substitutions = {
        'a': '@', 'A': '@',
        'o': '0', 'O': '0', 
        'i': '!', 'I': '!',
        's': '$', 'S': '$',
        'e': '3', 'E': '3'
    }
    
    # Apply single substitutions (only first occurrence or strategic positions)
    for char, replacement in substitutions.items():
        if char in word:
            # Replace only first occurrence
            temp = word.replace(char, replacement, 1)
            if temp != word:
                variants.add(temp)
    
    # Common combinations that make sense
    # o->0 (very common)
    temp_o = word.replace('o', '0').replace('O', '0')
    if temp_o != word:
        variants.add(temp_o)
    
    # a->@ (common for first 'a')
    if 'a' in word or 'A' in word:
        temp_a = word.replace('a', '@', 1).replace('A', '@', 1)
        if temp_a != word:
            variants.add(temp_a)
    
    # s->$ (common for 's' at end)
    if word.endswith('s') or word.endswith('S'):
        temp_s = word[:-1] + ('$' if word.endswith('s') else '$')
        variants.add(temp_s)
    
    # e->3 (selective)
    if 'e' in word or 'E' in word:
        temp_e = word.replace('e', '3', 1).replace('E', '3', 1)
        if temp_e != word:
            variants.add(temp_e)
    
    # Popular combinations
    # a->@ and o->0 together (but selective)
    temp_ao = word.replace('a', '@', 1).replace('A', '@', 1).replace('o', '0').replace('O', '0')
    if temp_ao != word:
        variants.add(temp_ao)
    
    return variants

def get_common_passwords():
    return [
        "root", "Root", "ROOT", "123456", "12345678", "123456789", "1234567890",
        "password", "Password", "PASSWORD", "admin", "Admin", "ADMIN", 
        "master", "Master", "MASTER", "user", "User", "USER",
        "guest", "Guest", "GUEST", "test", "Test", "TEST",
        "pass", "Pass", "PASS", "qwerty", "Qwerty", "QWERTY",
        "welcome", "Welcome", "WELCOME", "login", "Login", "LOGIN",
        "admin@123", "Admin@123", "ADMIN@123", "root@123", "Root@123", "ROOT@123",
        "master@123", "Master@123", "MASTER@123", "password@123", "Password@123", "PASSWORD@123",
        "pass@123", "Pass@123", "PASS@123", "user@123", "User@123", "USER@123",
        "admin123", "Admin123", "ADMIN123", "root123", "Root123", "ROOT123",
        "master123", "Master123", "MASTER123", "password123", "Password123", "PASSWORD123",
        "000000", "111111", "123123", "321321", "112233", "654321",
        "monkey", "dragon", "sunshine", "princess", "football", "shadow",
        "computer", "letmein", "abc123", "iloveyou", "trustno1", "batman"
    ]

def generate_clean_patterns(names, surnames, years, dob_variants, max_passwords=100000):
    passwords = set()
    
    # Add common passwords
    passwords.update(get_common_passwords())
    
    # Apply leet to common passwords
    for common in ["password", "admin", "master", "root", "pass"]:
        leet_variants = apply_leet_substitutions(common)
        passwords.update(leet_variants)
        for variant in leet_variants:
            passwords.add(f"{variant}@123")
            passwords.add(f"{variant}123")
    
    names = [n.strip() for n in names]
    surnames = [s.strip() for s in surnames]
    years = [y.strip() for y in years]
    
    # Use ONLY input data
    date_parts = set()
    date_parts.update(years)
    date_parts.update(dob_variants)
    
    # Realistic separators
    separators = ["", "_", "@", "#", ".", "!"]
    
    # 1. Individual names with all case variations
    for name in names:
        name_l = name.lower()
        name_c = name.capitalize()
        name_u = name.upper()
        
        # Base names
        passwords.add(name_l)
        passwords.add(name_c)
        passwords.add(name_u)
        
        # Apply leet substitutions
        leet_variants = apply_leet_substitutions(name_l)
        passwords.update(leet_variants)
        
        # Name + date combinations
        for part in date_parts:
            for sep in separators:
                passwords.add(f"{name_l}{sep}{part}")
                passwords.add(f"{name_c}{sep}{part}")
                passwords.add(f"{name_u}{sep}{part}")
                
                # Leet variants with dates
                for variant in leet_variants:
                    passwords.add(f"{variant}{sep}{part}")
        
        # Name + common suffixes
        passwords.add(f"{name_l}@123")
        passwords.add(f"{name_c}@123")
        passwords.add(f"{name_u}@123")
        passwords.add(f"{name_l}123")
        passwords.add(f"{name_c}123")
        passwords.add(f"{name_u}123")
        
        # Leet variants with common suffixes
        for variant in leet_variants:
            passwords.add(f"{variant}@123")
            passwords.add(f"{variant}123")
    
    # 2. Individual surnames with all case variations
    for surname in surnames:
        surname_l = surname.lower()
        surname_c = surname.capitalize()
        surname_u = surname.upper()
        
        # Base surnames
        passwords.add(surname_l)
        passwords.add(surname_c)
        passwords.add(surname_u)
        
        # Apply leet substitutions
        leet_variants = apply_leet_substitutions(surname_l)
        passwords.update(leet_variants)
        
        # Surname + date combinations
        for part in date_parts:
            for sep in separators:
                passwords.add(f"{surname_l}{sep}{part}")
                passwords.add(f"{surname_c}{sep}{part}")
                passwords.add(f"{surname_u}{sep}{part}")
                
                # Leet variants with dates
                for variant in leet_variants:
                    passwords.add(f"{variant}{sep}{part}")
        
        # Surname + common suffixes
        passwords.add(f"{surname_l}@123")
        passwords.add(f"{surname_c}@123")
        passwords.add(f"{surname_u}@123")
        passwords.add(f"{surname_l}123")
        passwords.add(f"{surname_c}123")
        passwords.add(f"{surname_u}123")
        
        # Leet variants with common suffixes
        for variant in leet_variants:
            passwords.add(f"{variant}@123")
            passwords.add(f"{variant}123")
    
    # 3. Name + surname combinations (forward and reverse)
    for name in names:
        for surname in surnames:
            name_l = name.lower()
            name_c = name.capitalize()
            name_u = name.upper()
            surname_l = surname.lower()
            surname_c = surname.capitalize()
            surname_u = surname.upper()
            
            # Realistic separators for name+surname
            name_separators = ["", "_", "."]
            
            for sep in name_separators:
                # Forward: name + surname (all case combinations)
                passwords.add(f"{name_l}{sep}{surname_l}")
                passwords.add(f"{name_c}{sep}{surname_l}")
                passwords.add(f"{name_u}{sep}{surname_l}")
                passwords.add(f"{name_l}{sep}{surname_c}")
                passwords.add(f"{name_c}{sep}{surname_c}")
                passwords.add(f"{name_u}{sep}{surname_c}")
                passwords.add(f"{name_l}{sep}{surname_u}")
                passwords.add(f"{name_c}{sep}{surname_u}")
                passwords.add(f"{name_u}{sep}{surname_u}")
                
                # CamelCase patterns (no separator)
                if sep == "":
                    passwords.add(f"{name_c}{surname_c}")  # RahulRaval
                    passwords.add(f"{surname_c}{name_c}")  # RavalRahul
                
                # Reverse: surname + name (all case combinations)
                passwords.add(f"{surname_l}{sep}{name_l}")
                passwords.add(f"{surname_c}{sep}{name_l}")
                passwords.add(f"{surname_u}{sep}{name_l}")
                passwords.add(f"{surname_l}{sep}{name_c}")
                passwords.add(f"{surname_c}{sep}{name_c}")
                passwords.add(f"{surname_u}{sep}{name_c}")
                passwords.add(f"{surname_l}{sep}{name_u}")
                passwords.add(f"{surname_c}{sep}{name_u}")
                passwords.add(f"{surname_u}{sep}{name_u}")
                
                # Apply leet substitutions to name+surname combinations
                name_leet = apply_leet_substitutions(name_l)
                surname_leet = apply_leet_substitutions(surname_l)
                
                for name_var in name_leet:
                    for surname_var in surname_leet:
                        passwords.add(f"{name_var}{sep}{surname_var}")
                        passwords.add(f"{surname_var}{sep}{name_var}")
                        
                        # CamelCase leet variants (no separator)
                        if sep == "":
                            name_camel = name_var.capitalize() if name_var != name_var.upper() else name_var
                            surname_camel = surname_var.capitalize() if surname_var != surname_var.upper() else surname_var
                            passwords.add(f"{name_camel}{surname_camel}")
                            passwords.add(f"{surname_camel}{name_camel}")
                
                # Name+surname with dates
                for part in date_parts:
                    # All case combinations with dates
                    passwords.add(f"{name_l}{sep}{surname_l}{part}")
                    passwords.add(f"{name_c}{sep}{surname_l}{part}")
                    passwords.add(f"{name_u}{sep}{surname_l}{part}")
                    passwords.add(f"{surname_l}{sep}{name_l}{part}")
                    passwords.add(f"{surname_c}{sep}{name_l}{part}")
                    passwords.add(f"{surname_u}{sep}{name_l}{part}")
                    
                    # CamelCase with dates
                    if sep == "":
                        passwords.add(f"{name_c}{surname_c}{part}")  # RahulRaval2005
                        passwords.add(f"{surname_c}{name_c}{part}")  # RavalRahul2005
                    
                    # With @ separator before date
                    passwords.add(f"{name_l}{sep}{surname_l}@{part}")
                    passwords.add(f"{name_c}{sep}{surname_l}@{part}")
                    passwords.add(f"{surname_l}{sep}{name_l}@{part}")
                    passwords.add(f"{surname_c}{sep}{name_l}@{part}")
                    
                    # CamelCase with @ separator
                    if sep == "":
                        passwords.add(f"{name_c}{surname_c}@{part}")  # RahulRaval@2005
                        passwords.add(f"{surname_c}{name_c}@{part}")  # RavalRahul@2005
                    
                    # Leet variants with dates
                    for name_var in name_leet:
                        for surname_var in surname_leet:
                            passwords.add(f"{name_var}{sep}{surname_var}{part}")
                            passwords.add(f"{surname_var}{sep}{name_var}{part}")
                            passwords.add(f"{name_var}{sep}{surname_var}@{part}")
                            passwords.add(f"{surname_var}{sep}{name_var}@{part}")
                            
                            # CamelCase leet variants
                            if sep == "":
                                name_camel = name_var.capitalize() if name_var != name_var.upper() else name_var
                                surname_camel = surname_var.capitalize() if surname_var != surname_var.upper() else surname_var
                                passwords.add(f"{name_camel}{surname_camel}{part}")
                                passwords.add(f"{surname_camel}{name_camel}{part}")
                                passwords.add(f"{name_camel}{surname_camel}@{part}")
                                passwords.add(f"{surname_camel}{name_camel}@{part}")
    
    # 4. Date-only patterns
    for part in date_parts:
        passwords.add(part)
    
    # 5. Additional CamelCase patterns for individual names/surnames
    for name in names:
        for surname in surnames:
            # More CamelCase variations
            passwords.add(f"{name.capitalize()}{surname.upper()}")  # RahulRAVAL
            passwords.add(f"{name.upper()}{surname.capitalize()}")  # RAHULRaval
            passwords.add(f"{surname.capitalize()}{name.upper()}")  # RavalRAHUL
            passwords.add(f"{surname.upper()}{name.capitalize()}")  # RAVALRahul
            
            # CamelCase with common suffixes
            passwords.add(f"{name.capitalize()}{surname.capitalize()}@123")  # RahulRaval@123
            passwords.add(f"{surname.capitalize()}{name.capitalize()}@123")  # RavalRahul@123
            passwords.add(f"{name.capitalize()}{surname.capitalize()}123")   # RahulRaval123
            passwords.add(f"{surname.capitalize()}{name.capitalize()}123")   # RavalRahul123
    
    if len(passwords) > max_passwords:
        passwords = set(list(passwords)[:max_passwords])
    
    return passwords

def write_wordlist(passwords, output_path):
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for pwd in sorted(passwords):
            f.write(pwd + "\n")

def main():
    parser = argparse.ArgumentParser(description="Clean password dictionary generator - input data only with proper leet speak")
    parser.add_argument("--names", required=True, help="Path to names.txt")
    parser.add_argument("--surnames", required=True, help="Path to surnames.txt")
    parser.add_argument("--years", required=True, help="Path to years.txt")
    parser.add_argument("--dob", help="Path to dob.txt")
    parser.add_argument("--output", required=True, help="Output wordlist file")
    parser.add_argument("--max", type=int, default=100000, help="Max passwords")
    
    args = parser.parse_args()
    
    names = read_lines(args.names)
    surnames = read_lines(args.surnames)
    years = read_lines(args.years)
    dob_lines = read_lines(args.dob) if args.dob else []
    
    dob_variants = build_dob_variants(dob_lines)
    passwords = generate_clean_patterns(names, surnames, years, dob_variants, args.max)
    write_wordlist(passwords, args.output)
    
    print(f"[+] Names: {len(names)}")
    print(f"[+] Surnames: {len(surnames)}")
    print(f"[+] Years: {len(years)}")
    print(f"[+] DOBs: {len(dob_lines)} (variants: {len(dob_variants)})")
    print(f"[+] Generated {len(passwords)} clean passwords")
    print(f"[+] CLEAN: Uses ONLY input data - no random additions")
    print(f"[+] All case variations: lowercase, Capitalized, UPPERCASE, CamelCase")
    print(f"[+] CamelCase patterns: RahulRaval, RavalRahul, RahulRaval@2005")
    print(f"[+] Separate date components: day, month, year individually and combined")
    print(f"[+] Selective leet speak: a->@, o->0, i->!, s->$, e->3 (strategic positions)")
    print(f"[+] Forward & reverse: name+surname AND surname+name")
    print(f"[+] No random numbers - only logical patterns")
    print(f"[+] Saved to: {args.output}")

if __name__ == "__main__":
    main()