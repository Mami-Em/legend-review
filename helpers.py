def rating_percentage(rating_frequencies):

    try:

        star = {
            '5': int(rating_frequencies['20']),
            '4': int(rating_frequencies['18']),
            '3': int(rating_frequencies['7']),
            '2': int(rating_frequencies['3']),
            '1': int(rating_frequencies['2'])
        }

        # total of review found
        total_rating = 0
        for i in star:
            total_rating += star[i]

        # for each star, calculate percentage
        rating_percent = [{i: round((star[i] * 100) / total_rating)} for i in  star]

    except:
        rating_percent = [0,0,0,0,0]


    return rating_percent


# %
def avg_rating(data):
    avg = float(data)
    return round(( avg * 5) / 100)


# /20
def avg_rating2(data):
    avg = float(data)
    return round(( avg * 5) / 20)

def main():
    print(rating_percentage({
        "2": "14",
        "3": "1",
        "4": "3",
        "7": "1",
        "8": "18",
        "9": "4",
        "10": "6",
        "11": "2",
        "12": "24",
        "13": "7",
        "14": "86",
        "15": "24",
        "16": "66",
        "17": "9",
        "18": "62",
        "19": "10",
        "20": "175"
      }))

main()