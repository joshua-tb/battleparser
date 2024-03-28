import sys
import time
from bs4 import BeautifulSoup
import html5lib
from jinja2 import Environment, FileSystemLoader


def input_roster():
    print('Roster file path: ')
    global ros_path 
    ros_path = input()
    print('Here is the roster path: ' + ros_path)
    print('Press Enter to continue.')
    input()
    open_roster()

def open_roster():
    try:    
        roster = open(ros_path, "r")
        roster
    except OSError as err:
            print(err)
            input_roster()
    else:
        print('Roster imported...')
    


input_roster()

force_names = []

abilities_table_dict = {}
feel_no_pain_dict = {}
force_factions_dict = {}
invuln_dict = {}
melee_table_dict = {}
model_table_dict = {}
ranged_table_dict = {}
selections_dict = {}
unit_table_dict = {}
keywords_dict = {}
sub_keywords_dict = {}

detachment_abilities_dict = {}
detachment_rules_dict = {}
faction_rules_dict = {}
rules_dict = {}
unit_rules_dict = {}

configuration_block_dict = {}




with open(f'{ros_path}') as roster:
#with open('Sisters (HTML).html') as roster:
    battle_soup = BeautifulSoup(roster, 'lxml')

force_tree = battle_soup.find_all("li", attrs={'class': 'force'})
rules_root = battle_soup.find("div", attrs={'class': 'summary'})
rules_p = rules_root.find_all("p")

number_of_forces = len(force_tree)

master_dict = {}
for forces in force_tree:
    working_force = forces.find("h2").text
    force_names.append(working_force)
    nested_categories = forces.find_all("li", attrs={'class': 'category'})
    categories_in_force = []
    uic_list = []
    units_in_force = []
    for cats in nested_categories:
        working_cat = cats.find("h3").text
        categories_in_force.append(working_cat)
        nested_units = cats.find_all("li", attrs={'class': 'rootselection'})
        units_in_category = []
        if "Configuration" in cats.h3:
            configuration_block_dict = { working_force : cats }
            continue
        for units in nested_units:
            working_unit = units.find("h4").text
            units_in_category.append(working_unit)
            units_in_force.append(working_unit)
            keywords_tree = units.find_all("p")
            sub_keywords_list = []
            unit_rules_list = []
            keywords_dict[working_unit] = units.find_all("p", limit=3)
            if units.ul is not None:
                if units.ul.li.ul is None:
                    sub_groups = units.ul.find_all("li")
                else:
                    sub_groups = units.ul.li.ul.find_all("li")
                for groups in sub_groups:
                    sub_group_rules_block = groups.find("p", attrs={'class': 'rule-names'})
                    if sub_group_rules_block is not None:
                        sub_group_rules_obj = sub_group_rules_block.find("span", attrs={'class': 'italic'}).contents
                        sub_group_rules_raw = sub_group_rules_obj[0].split(',')
                        for rule in sub_group_rules_raw:
                            working_rule = rule.strip()
                            if working_rule not in unit_rules_list:
                                unit_rules_list.append(working_rule)
                    sub_kw_raw = groups.text
                    sub_keywords = " ".join(sub_kw_raw.split())
                    sub_keywords_list.append(sub_keywords)
                sub_keywords_dict[working_unit] = sub_keywords_list
            #keywords_dict[working_unit] = units.find_all("p", limit=3)
            rules_block = units.find("p", attrs={'class': 'rule-names'})
            unit_rules_obj = rules_block.find("span", attrs={'class': 'italic'}).contents
            unit_rules_list_raw = unit_rules_obj[0].split(',')
            for rule in unit_rules_list_raw:
                working_rule = rule.strip()
                if working_rule not in unit_rules_list:
                    unit_rules_list.append(working_rule)
            unit_rules_dict[working_unit] = unit_rules_list
            for rule in unit_rules_list:
                if "Feel No Pain" in rule:
                    end = rule.index('+') ; end+=1
                    start = end-15
                    feel_no_pain_dict[working_unit] = rule[start:end]
            for table in units.find_all("table"):
                for string in table.strings:
                    if "Invulnerable Save" in string:
                        invuln_row = table.find(string="Invulnerable Save").parent.parent
                        invuln_desc = invuln_row.td.next_sibling.next_sibling.text
                        start = invuln_desc.index("+") ; start -= 1
                        end = start+2
                        invuln_dict[working_unit] = invuln_desc[start:end]
                for string in table.tr.th.strings:
                    if "Unit" in string:
                        table['class'] = "unit_data"
                        unit_table_dict[working_unit] = table
                    if "Melee" in string:
                        table['class'] = "melee_data"
                        melee_table_dict[working_unit] = table
                    if "Ranged" in string:
                        table['class'] = "ranged_data"
                        ranged_table_dict[working_unit] = table
                    if "Abilities" in string:
                        table['class'] = "abilities_data"
                        abilities_table_dict[working_unit] = table
        working_uic = {working_cat : units_in_category}
        uic_list.append(working_uic)
    uic_compile = {}
    for pairs in uic_list:
        uic_compile.update(pairs)
    #cif_compile = {"categories" : categories_in_force}
    uif_compile = {"units" : units_in_force}
    #list_compile = [ cif_compile, uic_compile ]
    master_dict[working_force] = uif_compile


rules_root = battle_soup.find_all("div", attrs={'class': 'summary'})
rules_p = []
for branches in rules_root:
    branch_rules = branches.find_all("p")
    for rules in branch_rules:
        rules_p.append(rules)


rule_names_raw = []
for rules in rules_p:
    rule_names_raw.append(rules.find("span").text)

rule_names = [names.replace(':', '') for names in rule_names_raw]
rules_dict = dict(zip(rule_names, rules_p))
for force in master_dict:
    detachment_rules = []
    detachment_rules_tree = configuration_block_dict[force].find("p", attrs={'class': 'rule-names'})
    if detachment_rules_tree is not None:
        detachment_rules = detachment_rules_tree.find("span", attrs={'class':'italic'}).contents
    detachment_tables = configuration_block_dict[working_force].find_all("table")
    if detachment_tables is not None:
        detachment_abilities = []
        for tables in detachment_tables:
            tables['class'] = "detachment_abilities_data"
            tables.th.string.replace_with("Detachment Abilities")
            detachment_abilities.append(tables)
        detachment_abilities_dict[force] = detachment_abilities
        unit_count = len(master_dict[working_force]['units'])
    for rule in rule_names:
        i = 0
        for unit in master_dict[working_force]['units']:
            if rule in unit_rules_dict[unit]:
                i += 1
            if i == unit_count:
                if rule not in detachment_rules:
                    detachment_rules.append(rule)
    if detachment_rules is not None:
        detachment_rules_dict[working_force] = detachment_rules
        for unit in master_dict[force]['units']:
            for rules in detachment_rules_dict[working_force]:
                if rules in unit_rules_dict[unit]:
                    rule_index = unit_rules_dict[unit].index(rules)
                    #unit_rules_dict[unit].pop(rule_index)
    for name,rule in rules_dict.items():
        rule_string = str(rule)
        if 'If your Army Faction is' in rule_string:
            faction_rules_dict[working_force] = {name:rule}
            for key in detachment_rules_dict[working_force]:
                if key in faction_rules_dict[working_force].keys():
                    i = detachment_rules_dict[working_force].index(key)
                    del detachment_rules_dict[working_force][i]
    for unit in master_dict[force]['units']:
        for keys in faction_rules_dict[working_force].keys():
            if keys in unit_rules_dict[unit]:
                rule_index = unit_rules_dict[unit].index(keys)
                unit_rules_dict[unit].pop(rule_index)
#    unit_count = len(master_dict[working_force]['units'])
#    for rule in rule_names:
#        i = 0
#        for unit in master_dict[working_force]['units']:
#            if rule in unit_rules_dict[unit]:
#                i += 1
#            if i == unit_count:
#                detachment_rules.append(rule)
#    if detachment_rules_dict[working_force] is not None:
#        detachment_rules_dict[working_force] = detachment_rules
#        for unit in master_dict[force]['units']:
#            for rules in detachment_rules_dict[working_force]:
#                if rules in unit_rules_dict[unit]:
#                    rule_index = unit_rules_dict[unit].index(rules)
#                    #unit_rules_dict[unit].pop(rule_index)



#for force in master_dict:
#    unit_count = len(master_dict[force]['units'])
#    army_rules =[]
#    for rule in rule_names:
#        i = 0
#        for unit in master_dict[force]['units']:
#            if rule in unit_rules_dict[unit]:
#                i += 1
#            if i == unit_count:
#                army_rules.append(rule)
#    force_rules = { force : army_rules }


env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("base_template.html")
new_file = f'{roster.name}_modified.html'

roster_content = template.render(
    master_dict = master_dict,
    unit_table_dict = unit_table_dict,
    invuln_dict = invuln_dict,
    feel_no_pain_dict = feel_no_pain_dict,
    ranged_table_dict = ranged_table_dict,
    melee_table_dict = melee_table_dict,
    abilities_table_dict = abilities_table_dict,
    detachment_abilities_dict = detachment_abilities_dict,
    unit_rules_dict = unit_rules_dict,
    keywords_dict = keywords_dict,
    sub_keywords_dict = sub_keywords_dict,
    rules_dict = rules_dict,
    detachment_rules_dict = detachment_rules_dict,
    faction_rules_dict = faction_rules_dict,
    configuration_block_dict = configuration_block_dict)

with open(new_file, mode='w', encoding="utf-8") as new_roster:
    new_roster.write(roster_content)
    print(f'Compiled and wrote {new_file}')




#unit_tables = []
#unit_rules = []
#unit_keywords = []
#raw_unit_tables_dict = {}
#for units in unit_tree:
#    unit_names.append(units.find("h4").text)
#    unit_tables.append(units.find_all("table"))
#    unit_rules.append(units.find("p", attrs={'class': 'rule-names'}))
#    unit_keywords.append(units.find("p", attrs={'class': 'category-names'}))
#    for string in units.p.strings:
#        if "Selections" in string:
#            selections_dict[units.p.parent.h4.text] = (units.p)
#
#
#raw_unit_tables_dict = dict(zip(unit_names, unit_tables))
#unit_rules_dict = dict(zip(unit_names, unit_rules))
#keywords_dict = dict(zip(unit_names, unit_keywords))
#
#
##search for invulns
#
#
#non_units = [ 'Battle Size', 'Detachment Choice', 'Show/Hide Options' ]
#for unwanted in non_units:
#    unit_names.remove(unwanted)
#    del raw_unit_tables_dict[unwanted]
#
#
#
#
#rule_names_raw = []
#for rules in rules_p:
#    rule_names_raw.append(rules.find("span").text)
#
#rule_names = [names.replace(':', '') for names in rule_names_raw]
#rules_dict = dict(zip(rule_names, rules_p))
#

