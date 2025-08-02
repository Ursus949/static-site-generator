from textnode import TextNode, TextType


# hello world
#print("hello world")

def main():
    node = TextNode("fn main(test)", TextType.CODE, "https://cht.sh/")
    print(node)


if __name__ == "__main__":
    main()
