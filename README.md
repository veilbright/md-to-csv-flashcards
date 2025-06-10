# Convert Markdown files to CSV

I use this script to write Anki flashcards faster; it won't cover every case and is geared towards the types of cards I usually create.

### How to format markdown file

```md
# Headers with one '#' are the front of cards

Anything else (after the first front) will go on the back of each card

# Unordered Lists can be added using dashes

- Use normal markdown formatting to ensure the lists are picked up correctly
- The dash must be at the very start of the line
- There must also be whitespace following the dash

# Ordered Lists can be added using numbered lists

1. The numbers must be a the very start of the line
2. There must be whitespace after the period
1. The actual numbers used doesn't matter

# Another type of list using descriptors can be added with dashes and colons

- New List: This list will not have bullet points, and bolds any text before the colon
- Formatting: The same rules apply as the unordered list

# Markdown tables will also be converted to HTML tables

| Formatting                                                                      | Style                                          |
|---------------------------------------------------------------------------------|------------------------------------------------|
| The only types of tables supported are those with a header, formatted like this | Some basic CSS styling is applied to the table |
| The fancy spacing isn't required                                                | Only a border and some padding                 |
```
