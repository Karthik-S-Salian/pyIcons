from typing import List,Union

NAME_SPACE = "http://www.w3.org/2000/svg"

def stringify_element(data):
    element = f"""<{data['tag']} {' '.join([f'{key} = "{values}"' for key,values in data.get('attr', {}).items()])} >"""
    for child_data in data.get("child", []):
        child_element = stringify_element(child_data)
        element+=child_element
    element+= f"</{data['tag']}>"
    return element


def create_svg_element(data,width:str="1em",height:str="1em",stroke:str="none",fill:Union[str,None]="black",stroke_width:str="0",class_names:List[str]=[],id:str=""):
    data["attr"]["width"] = width
    data["attr"]["height"] = height
    data["attr"]["xmlns"] = NAME_SPACE
    data["attr"]["stroke"] = stroke
    data["attr"]["fill"] = fill if fill else "none"
    data["attr"]["stroke-width"] = stroke_width
    data["attr"]["class"] = " ".join(class_names)
    data["attr"]["id"]  = id
    return stringify_element(data)
