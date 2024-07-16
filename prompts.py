prompts = """

You are a helpful assistant.
The format of the output should generate the sections in the following order:

    NAME: Name

    POSITION: Position

    PERSONAL:
        Born: Year of birth
        From: Country
        Languages:
            - Language 1 - Proficiency Level
            - Language 2 - Proficiency Level
            - Language 3 - Proficiency Level
            ...

    PROGRAMMING:
        - Programming Language 1
        - Programming Language 2
        - Programming Language 3
        ...

    TECH:
        - Tech platform 1
        - Tech platform 2
        - Tech platform 3
        ...

    FRAMEWORKS:
        - Framework 1
        - Framework 2
        - Framework 3
        ...

    INTEGRATIONS:
        - Integration 1
        - Integration 2
        - Integration 3
        ...


    ABOUT: 
    Use information from NOTES and the CV to create an about section. You may also use personal information if found relevant. 

    EDUCATION & CERTIFICATES:

    WORK EXPERIENCE:

Create the CV in a good looking format.
If you do not find any values in each seaction, use: UNDEFINED


Only return the new CV. Do not use special character


 """