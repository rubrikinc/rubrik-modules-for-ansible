
directory = "/Users/drew_russell/Google Drive/Development/Ansible/ansible/lib/ansible/modules/cloud/rubrik/"
filename = "rubrik_configure_dns_servers.py"


with open("{}{}".format(directory, filename)) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if line.strip() == "# Start Parameters":
            arugment_spec_upate_start = cnt
        elif line.strip() == "# End Parameters":
            arugment_spec_upate_end = cnt
        line = fp.readline()
        cnt += 1
    fp.close()


module_parameters = []
with open("{}{}".format(directory, filename)) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if (arugment_spec_upate_start + 3) <= cnt <= (arugment_spec_upate_end - 3):
            if line.strip() != "":
                module_parameters.append(line.strip())
        line = fp.readline()
        cnt += 1
    fp.close()

print("DOCUMENTATION = '''")
print("module: {}".format(filename.replace(".py", "")))
print("short_description: ")
print("description:")
print("    -")
print("version_added: 2.8")
print("author: Rubrik Ranger Team")
print("options:")

for param in module_parameters:
    indivdual_param = param[:-2].split("=dict(")
    option_name = indivdual_param[0]
    print("  " + option_name + ":")
    print("    description: ")
    if option_name == "timeout":
        print("      - The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.")
    else:
        print("      -")
    # print(indivdual_param[1])
    for param in indivdual_param[1].split(" "):
        if "aliases" in param:
            print(
                "    " +
                param.replace(
                    ",",
                    "").replace(
                    "'",
                    "").replace(
                    "=",
                    " = ").replace(
                    '"',
                    '').replace(
                        "[",
                        "").replace(
                            "]",
                            "").replace(
                                ' = ',
                    ": "))
        else:
            print(
                "    " +
                param.replace(
                    ",",
                    "").replace(
                    "'",
                    "").replace(
                    "=",
                    " = ").replace(
                    '"',
                    '').replace(
                        ' = ',
                    ": "))


print("\nextends_documentation_fragment:")
print("    - rubrik_cdm")
print("requirements: [rubrik_cdm]")
print("'''\n")
