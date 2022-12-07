import os
dirname = os.path.dirname(__file__)
image_path = 'static/prompt_image_uploads'
UPLOAD_FOLDER = os.path.join(dirname, image_path)







# # from app import app
# scavenger_hunts = {
#     'Mizzou_Quest': [
#         {
#             'clue': 1,
#             'prompt': 'Your MU Tigers work out here and you can too!\nFind this place.',
#             'coordinates': '38.94200875265407, -92.32646834504295',
#             'answer': 'Rec',
#         },
#         {
#             'clue': 2,
#             'prompt': 'Now that you have worked up a sweat, lets work out your brain. \n\nWhere would you go to borrow some books?',
#             'coordinates': '38.945311945553414, -92.32822378624653',
#             'answer': 'Ellis Library',
#         },
#         {
#             'clue': 3,
#             'prompt': 'Facts about this domed building: \n1. Function: Administrative Building.\n2. Adjacent concert auditorium.\n3. Featured on most Mizzou promotions.\nFind this location.',
#             'coordinates': '38.945311945553414, -92.32822378624653',
#             'answer': 'Jesse Hall',
#         },
#         {
#             'clue': 4,
#             'prompt': 'Here you will walk the Tiger Walk through these as a freshman and the Tiger Prowl as a senior. You should be pretty close by... \nFind the location of this MU tradition.',
#             'coordinates': '38.946655199979766, -92.32879005760252',
#             'answer': 'Columns',
#         },
#         {
#             'clue': 5,
#             'prompt': 'To eat pizza, or not to eat pizza? There really is no question. \nHead to the best pizza place in town.',
#             'coordinates': '38.948637004293545, -92.32788402343294',
#             'answer': 'Shakespeares Pizza',
#         }],
#     'Hannibal_Hunt': [
#         {
#             'clue': 1,
#             'prompt': 'Does a boy get a chance to whitewash a fence every day? Enter the last word on the sign located here.',
#             'coordinates': '39.71195081958449, -91.35780176501078',
#             'answer': 'Done',
#         },
#         {
#             'clue': 2,
#             'prompt': 'Hannibals oldest, family restaurant has been serving the downtown for four generations. They have an iconic sign spinning mug in their parking lot. What do they serve out of their mug?',
#             'coordinates': '39.71207977376028, -91.35859090451727',
#             'answer': 'Root Beer',
#         },
#         {
#             'clue': 3,
#             'prompt': '"...Now and then we had a hope that if we lived and were good, God would permit us to be pirates. These ambitions faded out, each in its turn; but the ambition to be a steamboatman always remained." \n- Life on the Mississippi, Mark Twain \nFind Mark Twain as a steamboatman. What does he say is his profession?',
#             'coordinates': '39.71253188272878, -91.35528171488045',
#             'answer': 'Steamboat Pilot',
#         },
#         {
#             'clue': 4,
#             'prompt': 'Hannibal has over a dozen public murals. Some are over 30 feet tall! One features a woman about to board a train. What color is her dress?',
#             'coordinates': '39.71074090151194, -91.35611319952365',
#             'answer': 'Green',
#         },
#         {
#             'clue': 5,
#             'prompt': 'Did you know that the light house in Hannibal is strictly decorative? Riverboats do not need it. But when it was installed in 1935 President FDR pushed a button a the White House to light it for the first time. How many steps is it to the lighthouse from Main Street?',
#             'coordinates': '39.714603033439445, -91.35896606556047',
#             'answer': '244',
#         }]
# }


# def getClue(scavenger_hunts, game, id):
#     clues = scavenger_hunts[game]
#     total = len(clues)
#     if id < total:
#         clue = clues[id] 
#         clue_id = clue['clue']
#         prompt = clue['prompt']
#         coordinates = clue['coordinates']
#         answer = clue['answer']
#     else:
#         clue_id = -1
#         prompt = f"Congrats! You have completed {game}."
#         coordinates = ""
#         answer = ""
#     return clue_id, prompt, coordinates, answer



# clue = getClue(scavenger_hunts, "MizzouQuest", 0)
# print(clue[0])


