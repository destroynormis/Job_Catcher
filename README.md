# JobCatcher

Telegram bot for catching IT vacancies from HH.ru with AI-powered profile analysis.

## About

JobCatcher is an asynchronous Telegram bot built with aiogram 3 that collects your professional profile (using Yandex GPT) and automatically searches for relevant IT vacancies on HH.ru.

The bot turns job hunting into a systematic pipeline: smart profile gathering → targeted search → clean vacancy cards.

## Features

- Natural AI interview to build your profile (Yandex GPT)
- Real-time vacancy search via official HH.ru API
- Filtering by skills, experience, salary and location
- Clean HTML-formatted vacancy output
- Modular architecture (routers + services + FSM)
- Ready for background notifications and database integration

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/destroynormis/Job_Catcher.git
   cd Job_Catcher
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment template
   ```bash
   cp .env.example .env
   ```
   Fill in your tokens (Telegram Bot Token + Yandex GPT API key).

5. Run the bot
   ```bash
   python -m bot.main
   ```

## Project Structure

```
bot/
├── handlers/     # Telegram routers
├── services/     # hh_service, ai_service
├── keyboards/
├── models/       # FSM states
├── utils/
├── main.py
└── config.py
```

## Roadmap

- [ ] Background vacancy notifications (APScheduler)
- [ ] Persistent storage (PostgreSQL / SQLite + Redis)
- [ ] AI-based vacancy relevance scoring
- [ ] Additional sources (Habr Career, SuperJob)
- [ ] Docker + docker-compose setup
- [ ] Webhook deployment

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)
