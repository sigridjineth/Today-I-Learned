#To learn classmethod & static method
class Language:
    default_language = "English"

    def __init__(self):
        self.show = "나의 언어는" + self.default_language

    @classmethod
    def class_my_language(cls):
        return cls()

    @staticmethod
    def static_my_language():
        return Language()
    
    def print_language(self):
        print(self.show)

class KoreanLanguage(Language):
    default_language = "Korean"

print(a.print_language())
print(b.print_language())