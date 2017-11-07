import aratext.extract_data as ed
import aratext.extract_data_with_itinerary as edi
# ed.extract_tri_route("../../Data/Shamela_0023696", "../../Data/Muqaddasi/muq_triples_route")
# ed.extract_tri_route("/home/rostam/Desktop/Chiara/It.Ant. - tagged_new",
#                      "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_tri")
# edi.extract_tri_route_WIt("/home/rostam/Desktop/Chiara/It.Ant. - tagged_new",
#                      "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_it_tri")
# ed.extract_route_wReg("../../Data/Shamela_0023696", "../../Data/Muqaddasi/muq_triples_route_wReg", "#$#FROM")

# extract the toponyms in FRIT and TOIT
edi.extract_iti_route("/home/rostam/Desktop/Chiara/It.Ant. - tagged_new",
                     "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_itiTopos")