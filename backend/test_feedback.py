from agents.feedback_agent.agent import (
    run_feedback_agent
)


feedback_events = [

    {
        "event_type": "wore",

        "outfit": {

            "occasion": "college",

            "items": [

                {
                    "id": "W001",
                    "category": "shirt",
                    "color": "white",
                    "fit": "oversized",

                    "style": [
                        "minimal",
                        "comfortable"
                    ],

                    "occasion": [
                        "college"
                    ]
                }
            ]
        }
    },


    {
        "event_type": "rating",

        "rating": 5,

        "outfit": {

            "occasion": "college",

            "items": [

                {
                    "id": "W001",
                    "category": "shirt",
                    "color": "white",
                    "fit": "oversized",

                    "style": [
                        "minimal",
                        "comfortable"
                    ],

                    "occasion": [
                        "college"
                    ]
                }
            ]
        }
    },


    {
        "event_type": "like",

        "outfit": {

            "occasion": "college",

            "items": [

                {
                    "id": "W001",
                    "category": "shirt",
                    "color": "white",
                    "fit": "oversized",

                    "style": [
                        "minimal",
                        "comfortable"
                    ],

                    "occasion": [
                        "college"
                    ]
                }
            ]
        }
    },


    {
        "event_type": "regenerate",

        "outfit": {

            "occasion": "office",

            "items": [

                {
                    "id": "W010",
                    "category": "blazer",
                    "color": "black",
                    "fit": "fitted",

                    "style": [
                        "formal"
                    ],

                    "occasion": [
                        "office"
                    ]
                }
            ]
        }
    },


    {
        "event_type": "dislike",

        "outfit": {

            "occasion": "office",

            "items": [

                {
                    "id": "W010",
                    "category": "blazer",
                    "color": "black",
                    "fit": "fitted",

                    "style": [
                        "formal"
                    ],

                    "occasion": [
                        "office"
                    ]
                }
            ]
        }
    }
]


result = run_feedback_agent(
    feedback_events
)


print(
    "\n\nFINAL RESULT:"
)

print(
    result
)