from unittest import result
from bs4 import BeautifulSoup
from .misc import str2float, datetime_formater, time_formater


def double_element_parser(element):
    data = {}
    soup = (BeautifulSoup(element, "html.parser").get_text()).replace("\n"," ")
    line_array = [s.replace(":","") for s in soup.split(" ") if s]

    data["b_red"] = str2float(line_array[3])
    data["b_white"] = str2float(line_array[6])
    data["b_black"] = str2float(line_array[9])
    data["b_total"] = str2float(line_array[12])

    if line_array[14] == "Preto": color = "black"
    if line_array[14] == "Vermelho": color = "red"
    if line_array[14] == "Branco": color = "white"

    data["r_color"] = color
    data["r_number"] = int(line_array[15])
    data["r_paid"] = str2float(line_array[18])
    data["r_keep"] = str2float(line_array[21])

    if line_array[25] == "Prejuizo!": status = "loss"
    if line_array[25] == "Lucro!": status = "profit"

    data["status"] = status
    data["date"] = line_array[26]
    data["datatime"] = time_formater(" ".join([line_array[26], line_array[28]]))
    data["timestamp"] = datetime_formater(data["datatime"])
    data["seed"] = line_array[31]

    return data