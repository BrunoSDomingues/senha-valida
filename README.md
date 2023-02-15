# Backend para verificar se uma senha é válida

A API contida neste repositório foi desenvolvida em Python utilizando o Flask para criar as rotas e o Graphene para gerar o schema de GraphQL.

## Estrutura dos arquivos

📦api
 ┣ 📜app.py (contém a estrutura principal da aplicação)
 ┗ 📜schema.py (contém a estrutura de schema usada como entrada)

## Como instalar o projeto

1. Clone este repositório usando o comando `git clone`
2. Abra um terminal na pasta onde clonou o repositório
3. Crie um virtual environment usando o comando `python -m venv my_app` (você pode dar outro nome se quiser)
4. Ative o virtual environment usando o comando `source my_app/bin/activate` (Linux/Mac) ou `my_app/Scripts/activate.bat` (Command Prompt do Windows) ou `my_app/Scripts/activate.ps1` (Powershell do Windows)
5. Instale os pacotes requeridos através do comando `python -m pip install -r requirements.txt`
6. Por fim, execute o comando `python api/app.py` e a aplicação estará disponível para uso

## Modo de usar

Para usar a aplicação, basta enviar uma request do tipo `POST` para a URL `localhost:8080/graphql` através do Postman (ou outra aplicação de sua preferência).

A request tem um body em formato GraphQL, e ele segue a estrutura abaixo:

```GraphQL
query {
    verify(password: "TesteSenhaForte!123&", rules: [
        {rule: "minSize", value: 8},
        {rule: "minSpecialChars", value: 2},
        {rule: "noRepeted", value: 0},
        {rule: "minDigit", value: 4}
    ]) 
    {
        verify
        noMatch
    }
}
```

Os campos que podem ser alterados são:

- `password`: a senha que o usuário deseja validar
- `rules`: a lista de regras que o usuário deseja testar, sempre no formato `{rule: "regra" (string), value: valor (inteiro)}`

O usuário pode testar as seguintes regras:

- `minSize`: tem pelo menos `x` caracteres.
- `minUppercase`: tem pelo menos `x` caracteres maiúsculos
- `minLowercase`: tem pelo menos `x` caracteres minúsculos
- `minDigit`: tem pelo menos `x` dígitos (0-9)
- `minSpecialChars`: tem pelo menos `x` caracteres especiais (os caracteres da seguinte string: `"!@#$%^&*()-+\/{}[]"`)
- `noRepeted`: não tenha nenhum caractere repetido em sequência ( ou seja, "aab" viola esta condição, mas "aba" não)

A saída gerada tem o formato abaixo (em JSON):

```JSON
{
    "data": {
        "verify": {
            "verify": false,
            "noMatch": [
                "minDigit"
            ]
        }
    }
}
```

onde:

- `verify`: indica se a senha está de acordo com as regras (true/false)
- `noMatch`: indica quais as regras violadas
