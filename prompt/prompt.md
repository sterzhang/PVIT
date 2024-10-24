# Prompt

## Prompt for MLLMs

### Holistic Information
```
<image>\nProvide a detailed description of this image, with special emphasis on the main character, including
their appearance, expressions, actions, and any distinguishing features.
```

### Personal Information
```
<image>\nDescribe the person in this image. Focus on the person\'s main features. Do not include any background information. In your response, you need to use <name> to refer to the person you describe when you mention the person\'s name first time. Do contain <name> in your response.
```

## Prompt for LLMs
### Dual-Level Information Fusion
```
# TASK DESCRIPTION
Given the Person Description of a person and the Holistic Description of the whole image, you need to put the placeholder <name> in the Holistic Description to represent the person described in Person Description. You should reply start with "Integrated Description: ".

# EXAMPLE 
Person Description: <name> is sitting in a relaxed posture. <name> is wearing a dark blue T-shirt and light blue jeans. On his left wrist, he has a watch. <name> is smiling and appears to be in a jovial mood. He is holding a blue object in his right hand, which looks like a piece of cloth or a towel. The background is a simple blue wall, and there is a light-colored blanket or couch behind him.\n
Holistic Description: The image captures a heartwarming moment between a man and a young boy. The man, wearing glasses and a blue shirt, is sitting on a couch, holding a blue balloon in his hand. He is smiling and looking at the boy, who is seated next to him. The boy, wearing a green shirt, is also smiling and looking at the man. The background of the image features a blue wall, adding to the overall warmth of the scene. The man's position on the left and the boy's on the right create a balanced composition. The blue balloon held by the man adds a playful element to the image. The smiles on their faces suggest a moment of joy and connection between the two.\n
Integrated Description: The image captures a heartwarming moment between <name> and a young boy. <name>, wearing glasses and a blue shirt, is sitting on a couch, holding a blue balloon in his hand. He is smiling and looking at the boy, who is seated next to him. The boy, wearing a green shirt, is also smiling and looking at <name>. The background of the image features a blue wall, adding to the overall warmth of the scene. <name>'s position on the left and the boy's on the right create a balanced composition. The blue balloon held by <name> adds a playful element to the image. The smiles on their faces suggest a moment of joy and connection between the two.

# TASK
Person Description: {pd}
Holistic Description: {hd}
```

### Choice QA Generation
```
# TASK DESCRIPTION
Now you need to generate multiple-choice questions based on a description of a person. You should pay particular attention to the characteristics mentioned in the description that describe this person, and use these characteristics to create questions and possible answers. You should reply start with "Generated MC: "

# RESPONSE FORMAT
Your response must strictly follow the format below (If there is nothing that can help you generate Q-A pair, then just reply with an empty []):\n
[[{"question": "…", "choices": ["…", "…", "…", "…"], "answer": "…"}]]

## ATTENTION
1. Please ensure that all references to the person in your questions and answers are replaced with the placeholder <name>. 
2. Only generate multiple-choice questions about the character.
3. Ensure that each set of choices has clear distinctions and no overlap to avoid multiple correct answers.

# IN-CONTEXT EXAMPLES
Example 1:
Information: In the photo, <name> is wearing a white shirt and blue jeans. She is standing and has her hands on her hips. She is also wearing a black bag.

Generated MC: [[{"question": "What color shirt is <name> wearing?", "choices": ["Red", "White", "Blue", "Black"], "answer": "White"}], [{"question": "What color are <name>'s jeans?", "choices": ["Black", "Green", "Blue", "Yellow"], "answer": "Blue"}], [{"question": "What is <name> doing with her hands?", "choices": ["Holding a bag", "Hands on her hips", "Waving", "In her pockets"], "answer": "Hands on her hips"}], [{"question": "What accessory is <name> wearing?", "choices": ["A hat", "A scarf", "A black bag", "Sunglasses"], "answer": "A black bag"}]]

Example 2:
Information: The image provided is blurry and lacks clear details, making it challenging to describe the person's clothing or actions accurately. The person's features are not distinctly visible, and there is no clear indication of what they might be wearing or doing. Due to the poor quality of the image, a detailed description cannot be provided.

Generated MC: []

# TASK
Information: {info}
Generated MC:
```

### Freeform QA Generation
```
# TASK DESCRIPTION
Now you need to generate question-and-answer data based on a description of a person. You should pay particular attention to the characteristics mentioned in the description that describe this person, and use these characteristics to create questions and answers. You should reply start with "Generated QA: "

# RESPONSE FORMAT 
Your response must strictly follow the format below(If there is nothing can help you generate Q-A pair, then just reply an empty []):\n
    [[{"question": "…", "answer": "…"}], [{"question": "…", "answer": "…"}]]

## ATTENTION 
Additionally, please ensure that all references to the person in your questions and answers are replaced with the placeholder <name>. And you only need to generate question and answer pair about the character.

# IN-CONTEXT EXAMPLES 
Example 1:
Information: In the photo, <name> is wearing a white shirt and blue jeans. She is standing and has her hands on her hips. She is also wearing a black bag.

Generated QA: [[{"question": "What color shirt is <name> wearing?", "answer": "White."}], [{"question": "What color are <name>'s jeans?", "answer": "Blue."}], [{"question": "What is <name> doing with her hands?", "answer": "<name> has her hands on her hips"}], [{"question": "What accessory is <name> wearing?", "answer": "<name> is wearing a black bag."}]]


Example 2:
Information: The image provided is blurry and lacks clear details, making it challenging to describe the person's clothing or actions accurately. The person's features are not distinctly visible, and there is no clear indication of what they might be wearing or doing. Due to the poor quality of the image, a detailed description cannot be provided.

Generated QA: []

# TASK
Information: {info}
Generated QA: 
```

### Witty QA Generation
```
# TASK DESCRIPTION 
Now you need to generate question-answer pairs based on a description of a person. You should pay particular attention to the characteristics mentioned in the description that describe this person, and use these characteristics to create some humorous and interesting questions and possible answers.

# RESPONSE FORMAT 
Your response must strictly follow the format below(If there is nothing can help you generate Q-A pair, then just reply an empty []):\n
    [[{"question": "…", "answer": "…"}], [{"question": "…", "answer": "…"}]]

## ATTENTION 
Additionally, please ensure that all references to the person in your questions and answers are replaced with the placeholder <name>. And you only need to generate question and answer pair about the character.

# IN-CONTEXT EXAMPLES 
Example 1:
Information: The person in the photo is <name>, a man standing on a rooftop. He is wearing a horizontally striped shirt with alternating light and dark brown stripes. The shirt is short-sleeved and has a collar. He is also wearing dark-colored work pants that appear to be stained with dirt or grime, suggesting he might have been working or engaged in some physical activity. The pants have pockets on the sides, and there is visible wear on the knees. He is flexing his muscles, raising his arms to show off his biceps, and has a confident expression on his face. He is positioned in the center of the image, drawing the viewer's attention immediately. The rooftop beneath his feet is made of red tiles, adding a vibrant splash of color to the scene. Behind him, the sky stretches out, a vast expanse of blue that provides a serene backdrop to the scene. A few clouds are scattered across the sky, adding depth and texture to the image. In the distance, beyond <name> and the rooftop, there are buildings visible, suggesting that the rooftop is part of a larger urban landscape. Overall, this image captures a moment of triumph or celebration, set against the backdrop of an urban skyline.


Generated QA: [[{"question": "What did <name> say to his dirty work pants before flexing his muscles?", "answer": ""You can't hold me down, grime! My biceps are here to save the day!""}],
[{"question": "Why does <name> flex his biceps on the rooftop?", "answer": "Because the city pigeons needed some fitness inspiration!"}],
[{"question": "What’s <name>'s secret to his confident rooftop pose?", "answer": ""It's all in the stripes! My shirt makes me look like a superhero.""}],
[{"question": "Why does <name> prefer to show off his muscles on rooftops?", "answer": ""Because the higher you go, the more impressive the flex!""}],
[{"question": "What’s <name> thinking while flexing on the rooftop?", "answer": ""Who needs a gym when you've got a rooftop and some heavy tiles?""}]]


Example 2:
Information: The image provided is blurry and lacks clear details, making it challenging to describe the person's clothing or actions accurately. The person's features are not distinctly visible, and there is no clear indication of what they might be wearing or doing. Due to the poor quality of the image, a detailed description cannot be provided.

Generated QA: []

# TASK
Information: {info}
Generated QA: 
```

### Reasoning QA Generation
```
# TASK DESCRIPTION 
Now you need to generate question-answer pairs based on a description of a person. You should pay particular attention to the characteristics mentioned in the description that describe this person, and create questions and answers that require reasoning and logical deductions.

# RESPONSE FORMAT 
Your response must strictly follow the format below(If there is nothing can help you generate Q-A pair, then just reply an empty []):\n
    [[{"question": "…", "answer": "…"}], [{"question": "…", "answer": "…"}]]

## ATTENTION 
Additionally, please ensure that all references to the person in your questions and answers are replaced with the placeholder <name>. And you only need to generate question and answer pair about the character.

# IN-CONTEXT EXAMPLES 
Example 1:
Information: The person in the photo is <name>, a man standing on a rooftop. He is wearing a horizontally striped shirt with alternating light and dark brown stripes. The shirt is short-sleeved and has a collar. He is also wearing dark-colored work pants that appear to be stained with dirt or grime, suggesting he might have been working or engaged in some physical activity. The pants have pockets on the sides, and there is visible wear on the knees. He is flexing his muscles, raising his arms to show off his biceps, and has a confident expression on his face. He is positioned in the center of the image, drawing the viewer's attention immediately. The rooftop beneath his feet is made of red tiles, adding a vibrant splash of color to the scene. Behind him, the sky stretches out, a vast expanse of blue that provides a serene backdrop to the scene. A few clouds are scattered across the sky, adding depth and texture to the image. In the distance, beyond <name> and the rooftop, there are buildings visible, suggesting that the rooftop is part of a larger urban landscape. Overall, this image captures a moment of triumph or celebration, set against the backdrop of an urban skyline.


Generated QA: [[{"question": "Why might <name> be wearing work pants with visible wear and dirt stains?", "answer": "The wear and dirt stains on <name>'s work pants suggest he might have been engaged in some form of physical labor or work, likely related to maintenance or construction."}],
[{"question": "What does <name>'s confident expression and muscle-flexing pose imply about his recent activities?", "answer": "The confident expression and muscle-flexing pose imply that <name> has recently completed a physically demanding task and is proud of his accomplishment."}],
[{"question": "What could be the reason for <name> standing on a rooftop instead of ground level?", "answer": "Standing on a rooftop might give <name> a sense of achievement and a better vantage point to view his surroundings, especially after completing a challenging task."}],
[{"question": "How do the alternating light and dark brown stripes on <name>'s shirt affect his appearance?", "answer": "The alternating light and dark brown stripes on <name>'s shirt add a visually interesting pattern that highlights his physique and draws attention to his upper body."}],
[{"question": "What might the presence of buildings in the background indicate about <name>'s location?", "answer": "The buildings in the background suggest that <name> is in an urban area, possibly working on a construction or maintenance project related to the city's infrastructure."}]]


Example 2:
Information: The image provided is blurry and lacks clear details, making it challenging to describe the person's clothing or actions accurately. The person's features are not distinctly visible, and there is no clear indication of what they might be wearing or doing. Due to the poor quality of the image, a detailed description cannot be provided.

Generated QA: []

# TASK
Information: {info}
Generated QA: 
```