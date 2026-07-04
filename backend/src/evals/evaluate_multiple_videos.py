from evals.push_to_db import push_eval_to_db
import asyncio
links={
    "Coding":[
        "https://www.youtube.com/watch?v=eJtD5vl00HA",
        "https://www.youtube.com/watch?v=6eBSHbLKuN0",
        "https://www.youtube.com/watch?v=p8Za5MtyVdg",
        "https://www.youtube.com/watch?v=8AWEPx5cHWQ"
    ],
    "News":[
        "https://www.youtube.com/watch?v=qKSXMDXOMek",
        "https://www.youtube.com/watch?v=65dNUm2f6NI",
        "https://www.youtube.com/watch?v=oHkE-B5Xhvc"
    ],
    "Podcast":[
        "https://www.youtube.com/watch?v=SfC-cnSgO1E",
        "https://www.youtube.com/watch?v=GYt5093aCQM&pp=0gcJCfwJAYcqIYzv",
        "https://www.youtube.com/watch?v=Pmd6knanPKw"
    ],
    "Interview":[
        "https://youtu.be/uCiBkaA4V6M?si=Y0bo4TZjYSBopyEA",
        "https://youtu.be/1qw5ITr3k9E?si=NUNHf42afFFZZwRz",
        "https://youtu.be/ZjmzEUY1x3Y?si=KacY9nljJS_yUQO6"
    ],
    "Comedy":[
        "https://youtu.be/1t1_a1BZ04o?si=A7YWPLq-wj1vG6rk",
        "https://youtu.be/314OLE6mKOo?si=i8paQVQrqH8V2Rj0",
        "https://youtu.be/W8-n2o8CaFU?si=eHANe5ADjlu3BXFO"
    ],
    "reality show":[
        "https://youtu.be/EU96s14zgLk?si=0a-frvrhbLpnurIz",
        "https://youtu.be/Do0kQEadPpA?si=FZkc8rbs-59fH_7L",
        "https://youtu.be/-Nwa2U-7sQA?si=qgi6dSe10vwbyPyP"
    ],
    "tutorials":[
        "https://www.youtube.com/watch?v=b-UZJVdLbXc",
        "https://www.youtube.com/watch?v=8wUUMOKAK-c&t=53s",
        "https://www.youtube.com/watch?v=wXvljefXyEo&t=3s"
    ],
    "cooking":[
        "https://www.youtube.com/watch?v=QL2tNKHB6ew",
        "https://www.youtube.com/watch?v=P6W8kwmwcno",
        "https://www.youtube.com/watch?v=i_164rISukM"
    ]
}

async def evaluate_videos():
    for category, videos in links.items():
        for video in videos:
            await push_eval_to_db(video)

asyncio.run(evaluate_videos())
