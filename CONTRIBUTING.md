# Contributing to Jarvis AI

Thank you for your interest in contributing to Jarvis AI!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs
- Include system information (OS, Python version)
- Provide steps to reproduce
- Include error messages and logs

### Feature Requests

- Open a GitHub Issue with the "enhancement" label
- Describe the feature and use case
- Explain how it fits the project goals

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Jarvis-ai-.git
cd Jarvis-ai-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

## Code Style

- Follow PEP 8
- Use Black for formatting: `black jarvis/`
- Run flake8 for linting: `flake8 jarvis/`
- Type hints encouraged: `mypy jarvis/`

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=jarvis tests/
```

## Adding New Features

### New Agent

1. Create file in `jarvis/agents/`
2. Inherit from `BaseAgent`
3. Implement required methods
4. Register in `AgentManager`
5. Add tests
6. Update documentation

### New Plugin

1. Create file in `jarvis/plugins/`
2. Inherit from `JarvisPlugin`
3. Implement manifest and execute methods
4. Register in `PluginManager`
5. Add tests
6. Update documentation

### New Tool Integration

1. Add to `shell_plugin.py` explanations
2. Or create dedicated plugin
3. Include teaching mode support
4. Add safety warnings
5. Test thoroughly
6. Document usage

## Documentation

- Update README.md for major features
- Update QUICKSTART.md for user-facing changes
- Add docstrings to all functions/classes
- Include usage examples

## Security

- Follow security best practices
- Never commit credentials
- Use policy engine for permissions
- Add appropriate warnings
- Test with restricted permissions

## Commit Messages

Use clear, descriptive commit messages:

```
Add nmap plugin with teaching mode support

- Implement NmapPlugin class
- Add scan type detection
- Include learning points
- Add comprehensive tool explanations
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Follow ethical hacking principles

## Legal

- Only contribute code you have rights to
- Respect licenses of dependencies
- Don't include copyrighted material
- Follow responsible disclosure for security issues

## Questions?

Open a GitHub Discussion or Issue for questions!

Thank you for contributing! 🎉
