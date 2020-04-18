# -*- coding: utf-8 -*-
import json

""" Reads the lyrics corpus in JSON and create seperate files for _data and for _posts """

file_name_structure = "2020-04-18-item-DIV_ID.md"
post_structure = """---
layout: post
title: TITLE
performer: PERFORMER
dialect: Sorani
audio: "AUDIO"

categories:
- CATEGORY

comments: true
---

<div class="language-plaintext highlighter-rouge">
    <div class="highlight">
        <pre class="highlight">
            <code>
        {% for line in site.data.itemDIV_ID.item.lg %}
        {{ line }}
        {% endfor %}
            </code>
        </pre>
    </div>
</div>

"""

json_structure = """
{
"item": {
  "head": "TITLE",
  "singer": "PERFORMER",
  "audio": "AUDIO",
  "lg": [TEXT]
}
}
"""

with open("KurdishLyricsCorpus.json") as f:
	corpus = json.load(f)

with open("else/audio_indices.tsv", "r") as f:
	audio_indices = {i.split("\t")[0]: i.split("\t")[2] for i in f.read().split("\n")}

for item in corpus["lyrics"]:
	item_post_file = post_structure
	item_json_file = json_structure
	item_json_content = list()
	lg = item["div"]

	# assign data 
	for key, value in {"TITLE": lg["head"], "PERFORMER": lg["singer"], "AUDIO": lg["audio"]}.items():
		if not len(value):
			value = "unassigned"
		item_post_file = item_post_file.replace(key, value)
		item_json_file = item_json_file.replace(key, value)

	# assign lyrics text
	for line in lg["lg"]:
		if type(line) == str:
			item_json_content.append(line)
		elif type(line) == list:
			item_json_content.extend(line)
		elif type(line) == dict:
			item_json_content.append(line["l"])
	item_json_file = item_json_file.replace("TEXT", ',\n\t'.join("\"{0}\"".format(x) for x in item_json_content))

	# assign category and ID
	item_post_file = item_post_file.replace("CATEGORY", audio_indices[item["@id"]])
	item_post_file = item_post_file.replace("DIV_ID", item["@id"])
	item_json_file = item_json_file.replace("DIV_ID", item["@id"])


	# save files
	with open("_posts/%s"%file_name_structure.replace("DIV_ID", item["@id"]), 'w', encoding='utf8') as f:
		f.write(item_post_file)

	with open("_data/item%s.json"%item["@id"], 'w', encoding='utf8') as f:
		f.write(item_json_file)

		



