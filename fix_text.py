with open ('lyrics/p2.txt', 'r') as f:
    text = f.read ()
    
    text = text.replace ("\n", " ")
    text = text.replace ("(", "")
    text = text.replace (")", "")
    text = text.replace (",", "")
    text = text.replace (" ", "\n")
    with open ('lyrics/p2.txt', 'w') as f2:
        f2.write (text)