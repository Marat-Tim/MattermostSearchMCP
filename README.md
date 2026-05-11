# MCP for searching in mattermost messages

## Main

For this to work, global search must be enabled in your Mattermost instance,
as MCP calls this feature via the API. 
The MCP 2 tool allows you to search for 
and retrieve the entire thread associated with a message(to understand the context).
This design reduces the number of calls to MCP and prevents it from getting confused by different IDs

## Config

The server URL must be specified in the MM_URL variable, for example, `https://mattermost.raiffeisen.ru`.


To work, the utility must call the Mattermost API. There are two authorization methods for this:                                                                                                              
1. Obtain an official Mattermost token and set it to the MM_TOKEN variable                                                                                                                                    
2. Retrieve the MMAUTHTOKEN, MMUSERID, and MMCSRF cookies from the browser and set them to the variables of the same name


If you have problem with ssl certificates you can set MM_VERIFY_SSL to                                                                                                                                        
- True(use default certificate)                                                                                                                                                                               
- False(do not use ssl)                                                                                                                                                                                       
- Raif_Default(certificate for raiffeisen mattermost instance)                                                                                                                                                
- Filepath with certificate                                                                                                                                                                                   
                      
## Install

### Global

Run outside of venv:
```shell
pip install git+https://github.com/Marat-Tim/MattermostSearchMCP.git
```
Then run
```shell
mm-search-mcp extract-auth-from-browser
```
Add printed variables to config and check
```shell
mm-search-mcp check
```
And add
```json
{
  "mcp": {
    "mm-search": {
      "type": "local",
      "command": [
        "mm-search-mcp",
        "run"
      ]
    }
  }
}
```

### Isolated(may works slow)

If you don't want download global packages you can use
```shell
uvx --from git+https://github.com/Marat-Tim/MattermostSearchMCP.git mm-search-mcp extract-auth-from-browser
```
```shell
uvx --from git+https://github.com/Marat-Tim/MattermostSearchMCP.git mm-search-mcp check
```
And then add
```json
{
  "mcp": {
    "mm-search": {
      "type": "local",
      "command": [
        "uvx",
        "--from",
        "git+https://github.com/Marat-Tim/MattermostSearchMCP.git",
        "mm-search-mcp",
        "run"
      ]
    }
  }
}
```
