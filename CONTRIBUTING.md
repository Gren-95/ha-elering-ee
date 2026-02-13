# Contributing to Elering Estonia Integration

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/Gren-95/ha-elering-ee/issues)
2. If not, create a new issue using the Bug Report template
3. Include as much detail as possible

### Suggesting Features
1. Check if the feature has already been suggested
2. Create a new issue using the Feature Request template
3. Explain your use case clearly

### Code Contributions

#### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/Gren-95/ha-elering-ee.git
cd ha-elering-ee

# Install Home Assistant (for testing)
pip install homeassistant

# Create a symbolic link to your Home Assistant config
ln -s $(pwd) ~/.homeassistant/custom_components/elering_ee
```

#### Making Changes
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

#### Code Style
- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to new functions/classes
- Keep functions focused and small

#### Testing
Before submitting a PR:
- [ ] Test the integration in a real Home Assistant instance
- [ ] Check that all Python files have valid syntax
- [ ] Verify manifest.json is valid JSON
- [ ] Update documentation if needed
- [ ] Update CHANGELOG.md

### Pull Request Process
1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with your changes
3. The PR will be merged once reviewed and approved

## Code of Conduct
- Be respectful and constructive
- Help others learn and grow
- Focus on what is best for the community

## Questions?
Feel free to open an issue for questions or reach out in discussions.

## Attribution
By contributing, you agree that your contributions will be licensed under the MIT License.
