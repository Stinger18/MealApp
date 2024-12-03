# What's for Dinner? 🍽️

An AI-powered meal planning assistant that helps you decide what to cook, leveraging LLM-based multi-modal agents to provide personalized recipe suggestions based on your ingredients, preferences, and dietary needs.

## Quick Links 🔗
- [Features](#features-)
- [Installation Guide](#getting-started-)
- [API Documentation](#api-endpoints-️)
- [Contributing](#contributing-)

## Overview 📖

What's for Dinner combines the power of large language models with a user-friendly interface to revolutionize your meal planning experience. Whether you're looking for quick recipes based on available ingredients or need comprehensive meal plans, our AI-powered system provides intelligent, personalized suggestions.

## Features 🌟

### Core Capabilities
- **AI-Powered Recipe Suggestions**
  - Personalized recommendations using LLM-based agents
  - Ingredient substitution suggestions
  - Dietary restriction awareness
  - Cooking time optimization

- **Smart Recipe Management**
  - Intelligent categorization
  - Dynamic search and filtering
  - Customizable recipe collections
  - Ingredient-based recipe matching

### User Experience
- **Intuitive Interface**
  - Clean, responsive design
  - Quick access to favorites
  - Real-time search suggestions
  - Mobile-friendly layout

## Technical Architecture 🏗️

### Backend Stack
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **SQLite** - Data storage
- **LLM Integration** - GPT-4 based recipe generation

### Frontend Stack
- **Modern Web Technologies**
  - HTML5/CSS3
  - JavaScript
  - Bootstrap
  - Fetch API

## Project Structure 📁
```
├── app/
│   ├── agent.py         # LLM-based AI agent
│   ├── crud.py          # Database operations
│   ├── database.py      # DB configuration
│   ├── main.py          # FastAPI application
│   ├── models.py        # Database models
│   └── schemas.py       # Data validation schemas
├── website/
│   └── index.html       # Web interface
└── requirements.txt     # Dependencies
```

## Getting Started 🚀

### Prerequisites
- Python 3.7+
- pip package manager
- OpenAI API key

### Quick Start
1. **Setup Environment:**
   ```bash
   git clone https://github.com/yourusername/whats-for-dinner.git
   cd whats-for-dinner
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create `.env` file:
   ```
   DATABASE_URL=sqlite:///./test.db
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Launch Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access:**
   - Web Interface: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## API Reference 📚

### Recipe Endpoints
```
GET    /recipes/         # List recipes
POST   /recipes/         # Create recipe
GET    /recipes/{id}     # Get recipe
PUT    /recipes/{id}     # Update recipe
DELETE /recipes/{id}     # Delete recipe
```

### AI Suggestion Endpoints
```
GET    /suggest/         # Get AI suggestions
GET    /suggest/quick    # Quick meal ideas
GET    /suggest/custom   # Personalized suggestions
```

## Development 👩‍💻

### Code Standards
- PEP 8 compliance
- Type hints required
- Comprehensive docstrings
- Unit test coverage

### Database Management
- Alembic migrations
- Regular backups
- Data validation

## Contributing 🤝

### Process
1. Fork repository
2. Create feature branch
3. Implement changes
4. Submit pull request

### Guidelines
- Write tests
- Update documentation
- Follow code style
- Keep changes focused

## Troubleshooting 🔧

### Common Issues
- **API Key Issues**: Verify OPENAI_API_KEY in .env
- **Database Errors**: Check DATABASE_URL configuration
- **Port Conflicts**: Use --port flag with uvicorn

## Roadmap 🗺️

### Upcoming Features
- [ ] Multi-user support
- [ ] Advanced meal planning
- [ ] Shopping list generation
- [ ] Mobile application
- [ ] Recipe sharing community

## License & Credits 📝

### License

```
MIT License

Copyright (c) 2024 Whats For Dinner Meal App

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Acknowledgments
- OpenAI for LLM capabilities
- FastAPI community
- SQLAlchemy team
- Project contributors
