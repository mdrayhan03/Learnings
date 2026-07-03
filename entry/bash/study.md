## The Shebang & Variables
Every script starts with a shebang, followed by your data definitions.
```bash
#!/bin/bash
# This is a comment

# ⚠️ CRITICAL SYNTAX: No spaces around the '=' sign when declaring variables
NAME="Senior Engineer"
AGE=30
READ_ONLY_VAR="Cannot change me"
readonly READ_ONLY_VAR

# Accessing variables requires a dollar sign ($)
echo "User: $NAME is $AGE years old."
```

## Reading Input and Arguments
Scripts often need data passed into them either interactively or via command-line arguments.

Positional Arguments
When you run ./script.sh arg1 arg2, Bash automatically assigns them to special numerical variables:

$0 = Name of the script itself

$1 = First argument (arg1)

$2 = Second argument (arg2)

$# = Total number of arguments passed

$@ = All arguments as a list

```bash
echo "Enter your deployment environment:"
read ENV_NAME
echo "Deploying to $ENV_NAME..."
```

## Conditional Statements (If / Else)
Bash conditional syntax uses square brackets [ ]. Spaces inside the brackets are mandatory.

String and Numeric Operators
Strings: == (equal), != (not equal), -z (is empty)

Numbers: -eq (equal), -ne (not equal), -lt (less than), -gt (greater than)
```bash
# ⚠️ Note the mandatory spaces: [ <space> condition <space> ]
if [ "$ENV_NAME" == "production" ]; then
    echo "⚠️ Warning: This is live!"
elif [ "$ENV_NAME" == "staging" ]; then
    echo "Deploying to test environment."
else
    echo "Unknown environment."
    exit 1 # Exit with an error code
fi
```
File Checking Operators (Incredibly Useful)
-f $FILE = True if the file exists and is a regular file.

-d $DIR = True if the directory exists.

-x $FILE = True if the file has execute permissions.
```bash
if [ -f "config.json" ]; then
    echo "Configuration found."
fi
```

## Loops (For and While)
Loops let you automate repetitive operations over files, arrays, or sequences.

For Loop (Iterating over a list or files)
```bash
# Loop through a predefined list
for server in web01 web02 web03; do
    echo "Pinging $server..."
done

# Loop through files in a directory
for file in *.log; do
    echo "Processing $file"
done
```
While Loop
```bash
COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Attempt $COUNT"
    COUNT=$((COUNT + 1)) # Math syntax (Double parentheses)
done
```

## Command Substitution & Math
Often you need to capture the output of a command or do simple arithmetic.

```bash
# 1. Command Substitution: $(command)
# Saves the output of 'date' or 'pwd' into a variable
CURRENT_TIME=$(date)
CURRENT_DIR=$(pwd)

# 2. Arithmetic Expansion: $(( expression ))
NUM1=10
NUM2=5
TOTAL=$((NUM1 + NUM2))
```

## Functions
Functions isolate code blocks to make your scripts modular and reusable.

```bash
# Function Definition
log_message() {
    # Functions use $1, $2 for their own internal arguments, 
    # independent of the main script arguments!
    local LEVEL=$1
    local MSG=$2
    echo "[$LEVEL] $(date): $MSG"
}

# Invoking a function (Do NOT use parentheses when calling)
log_message "INFO" "Database backup initiated."
log_message "ERROR" "Connection timed out."
```

## Exit Codes and Error Handling
Every Linux command returns an exit status between 0 (Success) and 255 (Error). You can catch this using the $? variable.

```bash
# Run a command
mkdir /root/secret_folder

# Check if it succeeded
if [ $? -eq 0 ]; then
    echo "Success!"
else
    echo "Failed! You probably lack sudo permissions."
fi
```

## Senior Pro-Tip: Safe Mode
Add this line right below your shebang in every script you write. It stops the script immediately if any command fails, preventing half-broken states:

```bash
set -e
```