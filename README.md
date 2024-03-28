# battleparser

Parses Battlescribe Army Rosters into a re-designed, card-style HTML layout for easier readability. Primary objective is to pair unit/model abilities and rules with their descriptions for easy reference.

How To Use BattleParser:

1: Create an Army Roster using BattleScribe
2: Export Army Roster in HTML format
3: Launch battleparser.py
4: When prompted, provide the path to your HTML Army Roster (path does not require quotes or escaping of special characters)

The re-formatted Army Roster will be saved in the same directory as the source file. It will have the same name with "_modified.html" appended, eg 'my-roster.html_modified.html'.

CSS includes styles for large screens (eg, desktops, laptops, tablets), small screens (eg, smartphones), and printed sheets. 

Battleparser does not interact with any real data sets and is essentially "dumb". There is no form of error checking to ensure that rules and stats are accurate -- it's only as good as the information provided. In some cases, the data used by BattleScribe may have minor errors or is otherwise incorrect -- this cannot be fixed by Battleparser and, in some circumstances, it may emphasize these errors. 

For example, the current (3/28/2024) data set for Battle Sister Squads in the Adepta Sororitas army contains a keyword error. The BSS Weapon Keywords are correct, but the Unit Keywords contains **Assault**. As such, the BSS unit card will list the **Assault** keyword in the Unit Rules even though that keyword is not applicable to any of their wargear / weapon profile options. Realistically, issues like this can only be fixed by those who maintain the data sets used by BattleScribe.

To-do's:

* Create a basic web front-end to replace using CLI
* Create Modified Roster feature options
    - Pair Leaders to Units
    - Enable/disable Army-wide Rules within Unit cards
    - Logic to check for duplicated Rules within Unit cards
    - Fix Invuln and FNP fields to be table rows (allows for correct, alternating background colors)
    - Floating menu/directory to quickly find Units
    - Dark Mode option
    - General clean-up and documentation