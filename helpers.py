import datetime

def d_format(date):
    y, m, nt = date.split('-')
    d, x = nt.split('T')
    m = datetime.datetime(int(y),int(m),int(d))

    return m.strftime('%B %d %Y')


def ratings(jsonRatings):

    try:
        newRatings = {
            '1': int(jsonRatings['3']),
            '2': int(jsonRatings['4']),
            '3': int(jsonRatings['5']), 
            '4': int(jsonRatings['19']), 
            '5': int(jsonRatings['20'])
        }

        vote = 0
        for i in newRatings:
            vote += newRatings[i]

        ratingsPercent = (newRatings['5']*100)/ vote

    except:
        return {
            'total_votes': 0,
            'avg_vote': 0
        }

    return {
        'total_votes': vote,
        'avg_vote': round(ratingsPercent*5)/100
    }

def format_rating(f):
    return round((f * 5)/20)