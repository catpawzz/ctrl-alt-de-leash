if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import SlashCommandGroup
import random
import datetime
import asyncio

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
    
    misc_group = SlashCommandGroup(name="misc", description="Miscellaneous fun commands")
    
    @misc_group.command(name="catify", description="Transforms your text into cat speak")
    async def catify(self, ctx, text: discord.Option(str, "Text to catify", required=True)):
        cat_words = ["nya", "meow", "purr", "mrow", "mrrp", "nyaa~", "prrp", "mew"]
        cat_emoticons = ["=^.^=", "ฅ^•ﻌ•^ฅ", "(=^･ω･^=)", "(^._.^)", "ㅇㅅㅇ"]
        
        # Process the text by words for better transformation
        words = text.split()
        catified_words = []
        
        for word in words:
            # Random stuttering (15% chance)
            if len(word) > 2 and random.random() < 0.15:
                word = word[0] + "-" + word
                
            # Basic letter replacements
            word = word.replace("r", "rrr")
            word = word.replace("R", "Rrr")
            word = word.replace("l", "w")
            word = word.replace("L", "W")
            
            # Random 'n' to 'ny' transformation (25% chance)
            if "n" in word and random.random() < 0.25:
                word = word.replace("n", "ny", 1)
            
            # Word replacements
            word_lower = word.lower()
            if word_lower in {"yes", "yeah", "yep"}:
                word = "purrhaps" if random.random() < 0.5 else "nyaes"
            elif word_lower in {"no", "nope"}:
                word = "nyo"
            elif word_lower in {"hello", "hi", "hey"}:
                word = random.choice(["henyo", "meowlo", "*purrs*"])
            elif word_lower == "good":
                word = "purrfect"
                
            catified_words.append(word)
        
        catified = " ".join(catified_words)
        
        # Add cat sounds to punctuation
        catified = catified.replace(".", f". {random.choice(cat_words)}~! ")
        catified = catified.replace("?", f"? {random.choice(cat_words)}~? ")
        catified = catified.replace("!", f"! {random.choice(cat_words)}~! ")
        
        # Add emoticon (30% chance)
        if random.random() < 0.3:
            position = random.choice(["start", "end"])
            emoticon = random.choice(cat_emoticons)
            if position == "start":
                catified = f"{emoticon} {catified}"
            else:
                catified = f"{catified} {emoticon}"
        
        # Ensure there's a cat sound at the end if no punctuation
        if not any(punct in catified for punct in ['.', '?', '!']):
            catified = f"{catified} {random.choice(cat_words)}~"
        
        await ctx.respond(f"{catified}")

    @misc_group.command(name="8ball", description="Ask the Magic 8-Ball a question")
    async def eightball(self, ctx, question: discord.Option(str, "Your question", required=True)):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes – definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ]
        
        response = random.choice(responses)
        embed = discord.Embed(
                title="🎱 Magic 8-Ball",
                color=discord.Color(0xe898ff)
                )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)

    @misc_group.command(name="choose", description="Choose between multiple options")
    async def choose(self, ctx, options: discord.Option(str, "Comma-separated options", required=True)):
        choices = [option.strip() for option in options.split(",") if option.strip()]
        
        if len(choices) < 2:
            await ctx.respond("Please provide at least two options separated by commas")
            return
        
        choice = random.choice(choices)
        await ctx.respond(f"🤔 I choose: **{choice}**")

    @misc_group.command(name="emojify", description="Convert text to emoji letters")
    async def emojify(self, ctx, text: discord.Option(str, "Text to convert", required=True)):
        char_map = {
            'a': '🅰', 'b': '🅱', 'c': '🆑', 'd': '🆔', 'e': '🅴', 'f': '🅵', 
            'g': '🅶', 'h': '🅷', 'i': '🅸', 'j': '🅹', 'k': '🅺', 'l': '🅻', 
            'm': '🅼', 'n': '🅽', 'o': '🅾', 'p': '🅿', 'q': '🆀', 'r': '🆁', 
            's': '🆂', 't': '🆃', 'u': '🆄', 'v': '🆅', 'w': '🆆', 'x': '🆇', 
            'y': '🆈', 'z': '🆉', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
            '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣',
            '?': '❓', '!': '❗', ' ': ' '
        }
        
        result = ''.join(char_map.get(c.lower(), c) for c in text)
        await ctx.respond(result)

    @misc_group.command(name="reverse", description="Reverses the given text")
    async def reverse(self, ctx, text: discord.Option(str, "Text to reverse", required=True)):
        reversed_text = text[::-1]
        await ctx.respond(reversed_text)

    @misc_group.command(name="drunkify", description="Makes text look like it was written by a drunk person")
    async def drunkify(self, ctx, text: discord.Option(str, "Text to drunkify", required=True)):
        result = ""
        words = text.split()
        drunk_phrases = ["*hic*", "*hiccup*", "...", "uhhh", "y'know?", "lol", "hahaa", "woooo", 
                         "*burp*", "lemme tell ya", "listen..", "i mean", "srsly", "omgg", 
                         "*stumbles*", "waiiit", "anywayy"]
        
        drunk_level = min(1.0, len(words) / 20)
        ending_phrases = ["*falls over*", "*passes out*", "im not drunk ur drunk", "one more drink plz",
                         "where am i??", "i love you guysss", "imma go home now", "whoooaaaa", 
                         "i feel siiiick", "don't tell my mom", "best night EVER"]
        
        typo_map = {
            'a': 'as', 'b': 'bv', 'c': 'cv', 'd': 'ds', 'e': 'er', 'f': 'fg', 'g': 'gf',
            'i': 'io', 'l': 'lk', 'm': 'mn', 'n': 'nm', 'o': 'op', 'p': 'po', 's': 'sd',
            't': 'ty', 'u': 'uy', 'v': 'vb', 'w': 'we', 'y': 'yu'
        }
        
        drunk_replacements = {
            'thanks': 'thankss', 'you': 'youu', 'hello': 'helloo', 'what': 'wut', 
            'love': 'luv', 'people': 'ppl', 'please': 'plz', 'though': 'tho',
            'definitely': 'def', 'probably': 'prolly', 'tonight': 'tonite',
            'the': 'teh', 'about': 'bout', 'going': 'goin'
        }
        
        i = 0
        while i < len(words):
            word = words[i]
            
            if random.random() < 0.15 * drunk_level:
                result += random.choice(drunk_phrases) + " "
            
            if word.lower() in drunk_replacements and random.random() < 0.7:
                word = drunk_replacements[word.lower()]
            
            if len(word) <= 2:
                result += word + " "
                i += 1
                continue
            
            drunk_word = list(word)
            
            for j in range(len(drunk_word) - 1):
                if random.random() < 0.2 * drunk_level:
                    drunk_word[j], drunk_word[j+1] = drunk_word[j+1], drunk_word[j]
            
            for j in range(len(drunk_word)):
                if random.random() < 0.1 * drunk_level and drunk_word[j].lower() in typo_map:
                    drunk_word[j] = random.choice(list(typo_map[drunk_word[j].lower()]))
                
                if random.random() < 0.2 * drunk_level:
                    drunk_word.insert(j, drunk_word[j])
            
            for j in range(len(drunk_word)):
                if random.random() < 0.15 * drunk_level:
                    drunk_word[j] = drunk_word[j].upper()
            
            j = 0
            while j < len(drunk_word):
                if random.random() < 0.1 * drunk_level and len(drunk_word) > 2:
                    drunk_word.pop(j)
                else:
                    j += 1
            
            result += "".join(drunk_word) + " "
            
            if random.random() < 0.08 * drunk_level:
                result += random.choice(["!", "?", "!!", "??", "!?", "....", "OMG"]) + " "
            
            if random.random() < 0.1 * drunk_level and i < len(words) - 1:
                result += words[i] + " "
            
            if random.random() < 0.05 * drunk_level and i < len(words) - 1:
                words_to_slur = min(2, len(words) - i - 1)
                slurred = "".join(words[i+1:i+1+words_to_slur])
                result += slurred + " "
                i += words_to_slur
            
            i += 1
            
        if random.random() < 0.4:
            result += random.choice(ending_phrases)
        
        await ctx.respond(result)
        
    @misc_group.command(name="formalify", description="Transforms casual text into formal, sophisticated language")
    async def formalify(self, ctx, text: discord.Option(str, "Text to formalize", required=True)):
        # Dictionary of contractions to expanded forms
        contractions = {
            "ain't": "is not", "aren't": "are not", "can't": "cannot", "couldn't": "could not", 
            "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not",
            "hasn't": "has not", "haven't": "have not", "he'd": "he would", "he'll": "he will", 
            "he's": "he is", "i'd": "I would", "i'll": "I shall", "i'm": "I am", "i've": "I have",
            "isn't": "is not", "it's": "it is", "let's": "let us", "mightn't": "might not",
            "mustn't": "must not", "shan't": "shall not", "she'd": "she would", "she'll": "she will",
            "she's": "she is", "shouldn't": "should not", "that's": "that is", "there's": "there is",
            "they'd": "they would", "they'll": "they will", "they're": "they are", "they've": "they have",
            "we'd": "we would", "we're": "we are", "we've": "we have", "weren't": "were not",
            "what'll": "what will", "what're": "what are", "what's": "what is", "what've": "what have",
            "where's": "where is", "who'd": "who would", "who'll": "who will", "who're": "who are",
            "who's": "who is", "who've": "who have", "won't": "will not", "wouldn't": "would not",
            "you'd": "you would", "you'll": "you will", "you're": "you are", "you've": "you have",
            "gonna": "going to", "wanna": "want to", "gotta": "got to", "sorta": "sort of",
            "kinda": "kind of", "dunno": "do not know", "y'all": "you all", "imma": "I am going to",
            "lemme": "let me", "gimme": "give me", "tryna": "trying to", "coulda": "could have", 
            "shoulda": "should have", "woulda": "would have", "musta": "must have", "'cause": "because",
            "'bout": "about", "'til": "until", "'em": "them", "d'you": "do you", "how'd": "how did", 
            "how's": "how is", "ma'am": "madam", "o'clock": "of the clock", "ol'": "old", 
            "whatcha": "what are you", "betcha": "bet you", "c'mon": "come on", "g'day": "good day", 
            "y'know": "you know", "whassup": "what is up", "wassup": "what is up",
            "ima": "I am going to", "finna": "fixing to", "hella": "very", "dontcha": "don't you",
            "gotcha": "got you", "ya": "you", "ur": "your", "u": "you", "r": "are", "idk": "I do not know",
            "tbh": "to be honest", "btw": "by the way", "brb": "be right back", "asap": "as soon as possible"
        }
        
        # Dictionary of casual words to formal equivalents
        casual_to_formal = {
            "yeah": "indeed", "yep": "affirmative", "nope": "negative", "ok": "acceptable",
            "okay": "satisfactory", "cool": "excellent", "awesome": "remarkable", 
            "great": "magnificent", "nice": "pleasant", "bad": "unfavorable",
            "good": "exceptional", "terrible": "abysmal", "huge": "substantial",
            "big": "considerable", "small": "diminutive", "pretty": "rather",
            "really": "genuinely", "very": "exceedingly", "just": "merely",
            "stuff": "materials", "things": "items", "guy": "gentleman",
            "guys": "individuals", "kids": "children", "everybody": "everyone",
            "totally": "completely", "amazing": "extraordinary", "sure": "certainly",
            "maybe": "perhaps", "guess": "surmise", "think": "believe",
            "thanks": "gratitude", "got": "obtained", "get": "acquire",
            "use": "utilize", "help": "assist", "show": "demonstrate",
            "tell": "inform", "buy": "purchase", "sell": "vend",
            "make": "create", "look": "appear", "see": "observe",
            "like": "appreciate", "want": "desire", "need": "require",
            "hi": "greetings", "hello": "salutations", "bye": "farewell",
            "weird": "unusual", "crazy": "irrational", "happy": "delighted",
            "sad": "melancholy", "mad": "irate", "scared": "apprehensive",
            "funny": "humorous", "love": "adore", "hate": "detest",
            "friend": "acquaintance", "enemy": "adversary", "money": "currency",
            "job": "profession", "work": "occupation", "house": "residence",
            "car": "vehicle", "food": "cuisine", "drink": "beverage",
            "anyway": "nevertheless", "lol": "[I find that amusing]", "omg": "[goodness gracious]",
            "dude": "esteemed individual", "bro": "dear fellow", "sis": "dear sister",
            "lit": "exceptionally impressive", "fire": "extraordinary", "sick": "impressive",
            "epic": "historically significant", "legit": "legitimate", "wack": "highly undesirable",
            "bomb": "superlative example", "basic": "unrefined", "extra": "unnecessarily excessive",
            "slay": "execute superbly", "flex": "ostentatiously display", "salty": "disgruntled", 
            "vibe": "ambience", "tea": "pertinent information", "shade": "subtle disparagement",
            "sus": "suspicious", "cap": "falsehood", "bet": "certainly", "chill": "relax",
            "fam": "respected associates", "trash": "substandard material", "ghosting": "deliberate avoidance",
            "squad": "close-knit group", "stan": "devoted admirer", "troll": "provocateur",
            "mood": "emotional state", "lowkey": "somewhat discreetly", "highkey": "rather overtly",
            "read": "critically analyze", "receipts": "evidence", "shook": "profoundly surprised",
            "snack": "visually appealing individual", "yikes": "expressing dismay", "wig": "astonishment",
            "cancel": "socially ostracize", "ship": "endorse romantically", "thirsty": "desperately eager",
            "hangry": "irritable due to hunger", "adulting": "fulfilling adult responsibilities",
            "feels": "emotional reactions", "bae": "beloved romantic partner", "boujee": "exhibiting refined taste",
            "catfish": "misrepresent identity", "savage": "harshly candid", "ok boomer": "I respectfully disagree",
            "spill the tea": "divulge information", "throw shade": "express subtle criticism",
            "left on read": "received communication without response", "hard pass": "firm refusal",
            "meh": "uninspiring", "yeet": "forcefully propel", "swag": "stylistic elegance",
            "totes": "absolutely", "srsly": "with utmost seriousness", "nbd": "inconsequential",
            "jk": "speaking facetiously", "tbh": "in candor", "fomo": "anxiety over missed experiences",
            "rage quit": "withdraw in frustration", "sips tea": "observes with interest",
            "same": "I concur completely", "literally": "precisely", "actually": "in point of fact",
            "basically": "fundamentally", "whatever": "regardless of which", "ugh": "[expressing discontent]",
            "fail": "disappointment", "win": "triumph", "lame": "uninspiring",
            "hot": "aesthetically pleasing", "old": "antiquated", "new": "contemporary", 
            "fake": "counterfeit", "smart": "intellectually gifted", "dumb": "intellectually challenged",
            "broke": "financially insolvent", "rich": "monetarily abundant"
        }
        
        # Formal phrases to occasionally insert
        formal_phrases = [
            "In light of this, ", "Consequently, ", "It is worth noting that ",
            "With all due respect, ", "If I may say so, ", "As a matter of fact, ",
            "It is my understanding that ", "I am of the opinion that ",
            "It is imperative to recognize that ", "I would like to emphasize that ",
            "One must consider that ", "It stands to reason that ",
            "From my perspective, ", "Taking everything into account, ",
            "In accordance with proper etiquette, ", "Upon further reflection, ",
            "Without a shadow of doubt, ", "As convention dictates, ", 
            "By all reasonable standards, ", "It behooves one to acknowledge that ",
            "Permit me to elucidate that ", "In the interest of full disclosure, ",
            "Empirical evidence suggests that ", "In the most respectful terms, ",
            "According to established precedent, ", "It is with great deference that I propose ",
            "Historical precedent indicates that ", "The logical conclusion is that ",
            "To express this in the most precise terms, ", "One cannot help but observe that ",
            "It would be remiss of me not to mention that ", "At the risk of belaboring the point, ",
            "To articulate my thoughts more clearly, ", "In keeping with the highest standards, ",
            "Bearing in mind the complexities involved, ", "Speaking objectively, ",
            "Drawing from extensive observations, ", "To put it most eloquently, ",
            "If one were to analyze this situation dispassionately, ", "In the grand scheme of things, ",
            "When all factors are duly considered, ", "Statistically speaking, ",
            "From a purely analytical standpoint, "
        ]
        
        # Formal closings
        formal_closings = [
            "Sincerely yours,", "With utmost respect,", "Most cordially,", 
            "With highest regards,", "I remain yours faithfully,",
            "With appreciation,", "Respectfully submitted,", "Yours truly,",
            "With sincere gratitude,", "I bid you good day.",
            "Most respectfully,", "With profound esteem,", "At your service,",
            "In your debt,", "With eternal gratitude,", "Your humble servant,",
            "Until our paths cross again,", "With distinguished consideration,", 
            "I have the honor to remain,", "With unwavering respect,",
            "In perpetual admiration,", "With the greatest deference,",
            "Ever at your disposal,", "With heartfelt appreciation,",
            "Remaining in your highest esteem,", "With the most distinguished sentiments,",
            "Ever faithful to your service,", "With boundless respect,",
            "I remain, as always, your loyal correspondent,", "With deepest regards,"
        ]
        
        # Process the text
        words = text.split()
        formalized_words = []
        
        # Add a formal opening (20% chance)
        if random.random() < 0.2:
            formalized_words.append(random.choice(formal_phrases))
        
        # Process each word
        i = 0
        while i < len(words):
            word = words[i]
            word_lower = word.lower()
            
            # Check for contractions - need to preserve capitalization
            contraction_found = False
            for contraction, expansion in contractions.items():
                if word_lower == contraction:
                    if word[0].isupper():
                        expansion = expansion[0].upper() + expansion[1:]
                    formalized_words.append(expansion)
                    contraction_found = True
                    break
            
            if contraction_found:
                i += 1
                continue
                
            # Check for casual words
            casual_found = False
            for casual, formal in casual_to_formal.items():
                if word_lower == casual:
                    if word[0].isupper():
                        formal = formal[0].upper() + formal[1:]
                    formalized_words.append(formal)
                    casual_found = True
                    break
            
            if casual_found:
                i += 1
                continue
            
            # If it's not a contraction or casual term, keep the original
            formalized_words.append(word)
            i += 1
            
            # Occasionally insert a formal phrase (10% chance per 5 words)
            if len(formalized_words) % 5 == 0 and random.random() < 0.1:
                formalized_words.append(random.choice(formal_phrases).strip())
        
        # Build the formalized text
        formalized = " ".join(formalized_words)
        
        # Clean up any double spaces
        formalized = formalized.replace("  ", " ")
        
        # Fix punctuation - ensure there's a space after commas and periods
        formalized = formalized.replace(",", ", ").replace(". ", ". ").replace("  ", " ")
        
        # Add period if there isn't one at the end
        if not formalized.endswith((".", "!", "?")) and len(formalized) > 0:
            formalized += "."
        
        # Capitalize first letter
        if len(formalized) > 0:
            formalized = formalized[0].upper() + formalized[1:]
        
        # Add formal closing (25% chance)
        if random.random() < 0.25 and len(formalized) > 10:
            formalized += "\n\n" + random.choice(formal_closings)
        
        await ctx.respond(formalized)
        
    @misc_group.command(name="randomize", description="Shuffles the order of words in your text")
    async def randomize(self, ctx, text: discord.Option(str, "Text to randomize", required=True)):
        words = text.split()
        
        if len(words) <= 1:
            await ctx.respond("Need at least two words to randomize!")
            return
            
        random.shuffle(words)
        
        result = " ".join(words)
        
        ending_punct = ""
        if text.endswith((".", "!", "?")):
            ending_punct = text[-1]
            if result and not result.endswith((".", "!", "?")):
                result += ending_punct
        
        if text[0].isupper() and result:
            result = result[0].upper() + result[1:]
                
        await ctx.respond(result)
        
    @misc_group.command(name="confuse", description="Transforms text to be confusing yet still readable")
    async def confuse(self, ctx, text: discord.Option(str, "Text to make confusing", required=True)):
        if not text:
            await ctx.respond("Please provide some text to confuse!")
            return
            
        result = ""
        
        similar_chars = {
            'a': ['а', 'α', 'ą', 'ä', 'å', 'ă', 'ā', 'ɑ'],
            'b': ['Ь', 'ß', 'ƀ', 'ɓ', 'ƅ', 'þ'],
            'c': ['с', 'ϲ', 'ƈ', 'ç', 'č', 'ć'],
            'd': ['ԁ', 'ɗ', 'đ', 'ď', 'ð'],
            'e': ['е', 'ε', 'ę', 'ë', 'ě', 'ɇ', 'ə'],
            'f': ['ƒ', 'ʄ', 'ғ'],
            'g': ['ɡ', 'ǥ', 'ğ', 'ǧ', 'ģ'],
            'h': ['һ', 'ħ', 'ɦ', 'ḥ'],
            'i': ['і', 'ɪ', 'ı', 'ï', 'í', 'ī', 'ĩ'],
            'j': ['ј', 'ʝ', 'ɉ', 'ĵ'],
            'k': ['ķ', 'ҟ', 'ҡ', 'қ'],
            'l': ['ӏ', 'ł', 'ľ', 'ļ', 'ḷ'],
            'm': ['м', 'ʍ', 'ṃ'],
            'n': ['ո', 'ņ', 'ň', 'ṇ', 'ń'],
            'o': ['о', 'ο', 'ȯ', 'ö', 'ô', 'ō', 'ø'],
            'p': ['р', 'ρ', 'ƥ', 'ṗ'],
            'q': ['զ', 'ԛ', 'ɋ'],
            'r': ['г', 'ɍ', 'ř', 'ŕ', 'ṛ'],
            's': ['ѕ', 'ʂ', 'š', 'ś', 'ş'],
            't': ['т', 'τ', 'ț', 'ť', 'ţ'],
            'u': ['υ', 'ս', 'ü', 'ú', 'ū', 'ũ'],
            'v': ['ν', 'ѵ', 'ṿ', 'ⱱ'],
            'w': ['ԝ', 'ѡ', 'ẁ', 'ẃ', 'ẅ', 'ⱳ'],
            'x': ['х', 'ҳ', 'ӽ', 'ẋ'],
            'y': ['у', 'γ', 'ý', 'ŷ', 'ÿ', 'ȳ'],
            'z': ['ʐ', 'ž', 'ź', 'ż', 'ƶ']
        }
        
        zalgo_marks = [
            '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306', '\u0307', 
            '\u0308', '\u0309', '\u030A', '\u030B', '\u030C', '\u030D', '\u030E', '\u030F', 
            '\u0310', '\u0311', '\u0312', '\u0313', '\u0314', '\u0315', '\u031A', '\u031B', 
            '\u033D', '\u033E', '\u033F', '\u0340', '\u0341', '\u0342', '\u0343', '\u0344', 
            '\u0346', '\u034A', '\u034B', '\u034C', '\u0350', '\u0351', '\u0352', '\u0357', 
            '\u035B', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368', '\u0369', 
            '\u036A', '\u036B', '\u036C', '\u036D', '\u036E', '\u036F', '\u0483', '\u0484', 
            '\u0485', '\u0486', '\u0487'
        ]
        
        weird_spacing = ['\u200B', '\u200C', '\u200D', '\u2060', '\u2063']
        
        confusion_level = min(1.0, len(text) / 40) * 0.8 + 0.2
        
        # Process character by character with occasional word transformations
        i = 0
        while i < len(text):
            char = text[i]
            
            # Special word-level transformations
            if char.isalpha() and random.random() < 0.15 * confusion_level:
                word_end = text.find(' ', i) if text.find(' ', i) != -1 else len(text)
                word = text[i:word_end]
                transformed_word = ""
                
                # Possible word transformations
                transform_type = random.choice([
                    'reverse', 'shuffle_middle', 'duplicate_random_letter', 'mix_case', 'normal'
                ])
                
                if transform_type == 'reverse' and len(word) > 2:
                    # Reverse the word but keep first and last letters
                    transformed_word = word[0] + word[-2:0:-1] + word[-1]
                    
                elif transform_type == 'shuffle_middle' and len(word) > 3:
                    # Keep first and last letters, shuffle the middle
                    middle = list(word[1:-1])
                    random.shuffle(middle)
                    transformed_word = word[0] + ''.join(middle) + word[-1]
                    
                elif transform_type == 'duplicate_random_letter' and len(word) > 1:
                    # Duplicate a random letter in the word
                    dup_index = random.randint(0, len(word) - 1)
                    transformed_word = word[:dup_index] + word[dup_index] + word[dup_index:]
                    
                elif transform_type == 'mix_case':
                    # Randomize the case of letters
                    transformed_word = ''.join(c.upper() if random.random() < 0.5 else c.lower() for c in word)
                    
                else:
                    transformed_word = word
                
                result += transformed_word
                i = word_end
                continue
                
            # Character level transformations
            if char.lower() in similar_chars and random.random() < 0.3 * confusion_level:
                # Replace with similar-looking character
                result += random.choice(similar_chars[char.lower()])
            else:
                result += char
                
            # Add zalgo effect (glitchy marks) with low probability
            if random.random() < 0.1 * confusion_level:
                num_marks = random.randint(1, 3 if confusion_level < 0.7 else 5)
                result += ''.join(random.choice(zalgo_marks) for _ in range(num_marks))
                
            # Add weird spacing with very low probability
            if random.random() < 0.05 * confusion_level:
                result += random.choice(weird_spacing)
                
            # Duplicate character with low probability
            if random.random() < 0.08 * confusion_level and char.isalpha():
                result += char
                
            # Insert typo with very low probability
            if random.random() < 0.03 * confusion_level and char.isalpha():
                nearby_keys = {
                    'a': 'sqzw', 'b': 'vghn', 'c': 'xdfv', 'd': 'scfre', 
                    'e': 'wsdr', 'f': 'dcvgr', 'g': 'fvbht', 'h': 'gbjny', 
                    'i': 'ujko', 'j': 'hknum', 'k': 'jlimo', 'l': 'kop;', 
                    'm': 'njk,', 'n': 'bmhj', 'o': 'iklp', 'p': 'ol;[', 
                    'q': 'asw', 'r': 'edft', 's': 'awedxz', 't': 'rfgy', 
                    'u': 'yhjki', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 
                    'y': 'tghu', 'z': 'xsda'
                }
                if char.lower() in nearby_keys:
                    result += random.choice(nearby_keys[char.lower()])
                
            i += 1
                
        await ctx.respond(result)

def setup(bot):
    bot.add_cog(MiscCog(bot))
