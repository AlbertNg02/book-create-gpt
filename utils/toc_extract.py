
def extract_table_of_contents(input_string):
    input_string = input_string.strip("'")

    # Evaluate the string as a Python expression
    output_list = eval(input_string)
    # output_list.pop(0)
    return output_list
