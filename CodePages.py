import xml.dom.minidom as _m
import re
import lxml.html
import lxml.etree
import os

class GenPlan():
    """docstring forGenPlan."""
    def __init__(self, dic_links):
        self.dict_links = dic_links

    def recup_plan(self, svg_path):
        image = _m.parse(svg_path)

        buttons = image.getElementsByTagName("g") #on récupère tout ce qui s'apparente à une image
        for button in buttons:
            if button.attributes["id"].value in self.dict_links.keys():
                childs = button.childNodes
                stroke = False
                j=0
                button.setAttribute("onclick", f"go_page('{self.dict_links[button.attributes['id'].value]}');")#va permettre d'appeler la fonction javascript change_state lors du click
                while j < len(childs) and not stroke:
                    child = childs[j]
                    if child.attributes!=None and "class" in child.attributes.keys():
                        if re.match("Strokebutton",child.attributes["class"].value):
                            child.setAttribute("class", "Button")#va permettre d'appeler la fonction javascript change_state lors du click
                            style_sans_fill = re.sub(r"fill:#\w+;",'',child.getAttribute("style"))
                            style_sans_fill_sans_stroke = re.sub(r"stroke:#\w+;",'',style_sans_fill)
                            child.setAttribute("style", style_sans_fill_sans_stroke)
                            stroke =True
                    j=j+1    
                    #Partie "front-end" et intéraction avec l'utilisateur
        #il est important de mettre l'argument "this" pour permettre au code javascript de reconnaître le bouton enquestion et le modifier
         #il y a un problème d'ordre: ls tyle de l'objet passe après la classe, ce qui fait que le style de la classe n'est paspris en compte
        #il faut donc régler cela en mettant supprimant la valeure stroke et fill du style de chaques chambres

        return image.toxml()

    def new_plan(self, svg_path, nom_du_plan):
        #récupération des bouttons
        f_b= self.recup_plan(svg_path)
        root_node = lxml.html.parse("Pages/PlanSqueletteHTML.html")

        div = root_node.find(".//div[@id='ImageSvg']") #. = le noeud courant , // = tous les éléments à partir de ce noeud
        #donne donc: je cherche tous les enfants de div où div a pour id 'main_plan'
        el = lxml.html.fromstring(f_b) #on récupère les éléments créés
        div.append(el)# on l'ajoute à notre principale partie

        # partie enregistrement de l'image +
        path = f'Pages/{nom_du_plan}.html'
        os.makedirs(os.path.dirname(path), exist_ok=True)#marche suelement avec python 3.2
        with open(path, "w") as f:
            f.write(lxml.html.tostring(root_node).decode("utf-8"))

        return path
g = GenPlan({"CopainVille":"CopainVille.html",
            "Barman": "Barman.html",
            "VendeurChinois": "VendeurChinois.html",
            "Cartographe": "Cartographe.html",
            "Animalistes": "Animalistes.html",
            "Chasseur":"Chasseur.html"
            })
g.new_plan("Svg/Garcon.svg", "Garcon")
