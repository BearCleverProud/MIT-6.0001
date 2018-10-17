import string
text="purple!!!!cow!!!!"
text=text.lower()
text_space=""
text_split=[]
for each in text:
    if each not in string.ascii_letters:
        text_space+=" "
    else:
        text_space+=each
text_split=text_space.split(" ")
while '' in text_split:
    text_split.remove('')
text_length=len(text_split)
print(text_split)
print(text_length)
