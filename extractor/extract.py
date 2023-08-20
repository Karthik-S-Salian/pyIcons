import re
from pathlib import Path
import json

REACT_ICONS_BASE_DIR = Path(__file__).parent.parent/"react-icons"

icons={}

def extractSvg(code,dir_name):
    # Define the regular expression pattern to match the function name and JSON object
    pattern = r'(\w+)\s*=\s*function\s*(\w+)\s*\(([^)]*)\)\s*{.*?GenIcon\((\{.*?\})\)\(props\);'

    # Find all occurrences of the pattern in the code
    matches = re.finditer(pattern, code, re.DOTALL)

    # Extract the function names and JSON objects from each match
    d={}
    for match in matches:
        function_name = match.group(2)
        json_object_str = match.group(4)
        d[function_name] = eval(json_object_str)

    if d:
        icons[dir_name] = d


for path in REACT_ICONS_BASE_DIR.iterdir():
    if not path.is_dir():
        continue

    js_path = path/"index.js"
    if not js_path.exists():
        continue

    print(path.stem)

    with open(js_path,"r") as fh:
        extractSvg(fh.read(),path.stem)

# with open(Path(__file__).parent/"svgIcons.json","w") as fh:
#     json.dump(icons,fh,indent=4)

# print("start writing python file")
# ICONS_PYTHON_FOLDER = Path(__file__).parent.parent/"pyIcons/icons"
# for key,values in icons.items():
#     with open(ICONS_PYTHON_FOLDER/f"{key}.py","w") as fh:
#         print(f"writing {key}.py ....")
#         content = ""
#         for iconName,icon in values.items():
#             content +=f"\n{iconName} = {icon}"
#         fh.write(content)


imports = """
from typing import List,Union
from ..utils import create_svg_element
"""
fun = """
def {}(width:str="1em",height:str="1em",stroke:str="none",fill:Union[str,None]="black",stroke_width:str="0",class_names:List[str]=[],id:str=""):
    return create_svg_element({},width,height,stroke,fill,stroke_width,class_names,id)
"""
print("start writing python file")
ICONS_PYTHON_FOLDER = Path(__file__).parent.parent/"pyIcons/icons"
for key,values in icons.items():
    with open(ICONS_PYTHON_FOLDER/f"{key}.py","w") as fh:
        print(f"writing {key}.py ....")
        content = imports
        for iconName,icon in values.items():
            content +=fun.format(iconName,icon)
        fh.write(content.strip())