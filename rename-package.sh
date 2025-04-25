package_rgx='[_a-zA-Z0-9\-]+'
oldname=$(grep -E "^ *name *= *\"${package_rgx}\"" pyproject.toml | grep -Eo "\"${package_rgx}\"" | sed s/\"//g)

if [ -z "$oldname" ]; then
    echo "old name not found"
    exit 1
fi

# Rename package to new name
find tests src docs .github/workflows pyproject.toml README.md Dockerfile -type f -exec sed -i s/$oldname/${1}/g {} +
mv src/$oldname src/$1

# Change URLs to new repo path
sed -i s/python-template/$(basename `git rev-parse --show-toplevel`)/g README.md

# Remove this file
rm -- "$0"