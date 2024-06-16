class Link:
    icon: str
    title: str
    desc: str
    url: str
    color: str

    def __init__(self, icon: str, title: str, desc: str, url: str, color: str):
        self.icon = icon
        self.title = title
        self.desc = desc
        self.url = url
        self.color = color
