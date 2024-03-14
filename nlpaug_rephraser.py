import nlpaug.augmenter.word as naw

class NLPAugRephraser:
    def __init__(self):
        self.aug = naw.SynonymAug(aug_src='wordnet')

    def rephrase(self, text):
        return self.aug.augment(text)
