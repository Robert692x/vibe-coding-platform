# ALGO AI LLM Architecture

## 1) System Prompt Layer
Defined in `ton_mind_bot/ai/system_prompt.py`.
Contains persona, communication style, safety rules, and capabilities.

## 2) Knowledge Base Layer
- Static knowledge block in `system_prompt.py`.
- Extended docs in `ton_mind_bot/ai/knowledge_base.md`.

## 3) Tools / MCP Layer (runtime integrations)
Current bot tools/services:
- Wallet checks and holder analytics
- TON market analytics and scanners
- Token growth notifications
- Premium/payment automation

## Prompt Runtime
`OpenAIService` composes messages as:
- system prompt
- knowledge block
- few-shot examples
- user message

This provides consistent ALGO AI behavior in Telegram chat.
