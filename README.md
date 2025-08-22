# Telegram Bulk Invite Tool

A comprehensive GUI-based tool for bulk inviting users to Telegram groups with advanced features for member extraction and file processing.

## Features

### 1. File Processing
- Import usernames from TXT or CSV files
- Remove duplicates automatically
- Validate Telegram usernames
- Sort usernames alphabetically
- Export processed lists

### 2. Bulk Invite
- Invite users to Telegram groups in bulk
- Configurable delays between invites
- Progress tracking with real-time updates
- Comprehensive error handling
- Stop/resume functionality
- Activity logging with timestamps

### 3. Member Extraction
- Extract members from existing Telegram groups
- Filter visible members only
- Extract users with usernames only
- Export extracted member lists

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Telegram API credentials:
   - Go to https://my.telegram.org
   - Create a new application
   - Get your API ID and API Hash
   - Update the values in the script

## Usage

1. Run the application:
```bash
python telegram_bulk_invite.py
```

2. **File Processing Tab:**
   - Select a file containing usernames (one per line)
   - Configure processing options
   - Process and save the cleaned list

3. **Bulk Invite Tab:**
   - Enter the target group invite link
   - Select the usernames file
   - Configure invite settings (delay, max invites)
   - Start the invite process

4. **Extract Members Tab:**
   - Enter source group link/username
   - Configure extraction settings
   - Extract and save member lists

## Important Notes

### Security & Ethics
- This tool is for educational and testing purposes only
- Always obtain proper authorization before inviting users
- Respect Telegram's Terms of Service and rate limits
- Be mindful of user privacy and consent

### Rate Limiting
- The tool includes built-in delays to prevent flood errors
- Telegram has strict rate limits for bulk operations
- Adjust delays based on your account's limitations

### Error Handling
- Comprehensive error handling for common issues:
  - User privacy restrictions
  - Flood wait errors
  - Invalid usernames
  - Network connectivity issues

## Configuration

### Default Settings
- Delay between invites: 30 seconds
- Maximum invites per session: 200
- API ID and Hash: Update in the script

### Customization
- Modify delay ranges in the code
- Adjust username validation patterns
- Configure proxy settings (if needed)

## Troubleshooting

### Common Issues
1. **"Invalid group invite link"**: Ensure the link format is correct (t.me/+... or t.me/joinchat/...)
2. **"Flood wait error"**: Reduce invite frequency or wait for the specified time
3. **"User privacy restricted"**: Some users have privacy settings that prevent invitations
4. **"Not a mutual contact"**: Some users only accept invites from contacts

### Performance Tips
- Use smaller batch sizes for better reliability
- Increase delays if encountering frequent errors
- Process username files before bulk inviting

## Legal Disclaimer

This tool is provided for educational purposes only. Users are responsible for:
- Obtaining proper authorization
- Complying with local laws and regulations
- Respecting Telegram's Terms of Service
- Ensuring user consent for invitations

The developers are not responsible for any misuse of this tool.
 
 
 
 
  
