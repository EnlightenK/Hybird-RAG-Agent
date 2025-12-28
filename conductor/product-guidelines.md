# Product Guidelines

## Conversational Tone & Style
- **Professional & Technical:** Responses must be direct, concise, and technically accurate. Avoid unnecessary conversational filler.
- **Data-Rich:** Include relevant source metadata and search scores where appropriate to provide context for the answers.

## Interface & Interaction
- **Transparent Execution:** The CLI must clearly display the internal steps taken by the agent, such as triggering a hybrid search or processing document chunks.
- **Real-Time Streaming:** Responses must be streamed to the terminal in real-time to provide immediate feedback to the user.

## Accuracy & Error Handling
- **No Hallucinations:** If no relevant information is found in the knowledge base, the agent must explicitly state that it cannot find an answer rather than attempting to guess.
- **Source Grounding:** All answers must be grounded in the retrieved document chunks.

## Visual Design
- **Structured Output:** Use formatting that emphasizes clarity and structure, ensuring that complex technical information is easy to parse.
