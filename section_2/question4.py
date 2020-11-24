import csv

# Assumptions: Each product must have at least one attribute


def generate_html(title, description, attributes):
    return f"<html><head><title>{title}</title></head><body>{description}<h1>Item Attributes</h1><ul>{attributes}</ul></body></html>"


def generate_description(description):
    if len(description.strip()) == 0:
        return ""
    return f"<h1>Description</h1><span>{description}</span>"


def generate_attribute_list(attributes):
    ul_contents = ""
    for attribute in attributes:
        if attribute != "":
            ul_contents += f"<li>{attribute}</li>"
    return ul_contents


def generate_items_html(input_csv, output_csv):
    output_content = []
    with open(input_csv, "r") as input_file:
        reader = csv.reader(input_file)
        # skip column names
        next(reader)
        for row in reader:
            description = generate_description(row[2])
            attribute_list = generate_attribute_list(row[3:])
            html_content = generate_html(row[1], description, attribute_list)
            output_content.append([row[0], html_content])

    with open(output_csv, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        # insert column names
        writer.writerow(["item_id", "html"])
        for item in output_content:
            writer.writerow(item)


if __name__ == "__main__":
    generate_items_html("./dataset_input.csv", "./dataset_output.csv")