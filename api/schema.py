from graphene import ObjectType, String, List, Field, Schema, Boolean
from graphene.types.generic import GenericScalar
from re import findall

special_chars = "!@#$%^&*()-+\/{}[]"  # Caracteres especiais


class VerifyType(ObjectType):
    # O output possui dois campos: verify (True/False) e noMatch (uma lista de strings indicando onde a validação falhou)
    verify = Boolean()
    noMatch = List(String)

    def resolve_verify(root, info):
        # Extraindo a senha e as regras escolhidas
        password = root["password"]
        rules = root["rules"]

        # Iterando sobre a lista de regras
        for r in rules:
            rule = r["rule"]  # Regra passada no campo rule
            value = r["value"]  # Numero passado no campo value

            # Usando o match case para cada uma das regras: se uma delas não foi cumprida, seta verify como False e adiciona a regra em noMatch
            match rule:
                case "minSize":
                    if len(password) < value:
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case "minUppercase":
                    if sum(1 for c in password if c.isupper()) < value:
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case "minLowercase":
                    if sum(1 for c in password if c.islower()) < value:
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case "minDigit":
                    if sum(1 for c in password if c.isdigit()) < value:
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case "minSpecialChars":
                    if sum(1 for c in password if c in special_chars) < value:
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case "noRepeted":
                    # Usando regex para verificar se encontra caraceteres repetidos adjacentes
                    if (
                        len([match[0] for match in findall(r"((\w)\2{1,})", password)])
                        > value
                    ):
                        root["verify"] = False
                        root["noMatch"].append(rule)

                case _:
                    continue

        return root["verify"]

    def resolve_nomatch(root, info):
        # Como o noMatch foi incluso no resolver acima, apenas repassa o valor
        return root["noMatch"]


class Query(ObjectType):
    # Cria um Field do tipo a ser verificado, passando os argumentos de entrada (senha e lista de regras)
    verify = Field(
        VerifyType,
        password=String(required=True),
        rules=List(GenericScalar, required=True),
    )

    def resolve_verify(root, info, password, rules):
        # Objeto de dados que é repassado entre os resolvers
        DATA = {
            "verify": True,
            "noMatch": [],
            "password": "",
            "rules": [],
        }

        # Define os campos password e rules para os resolvers processarem
        DATA["password"] = password
        DATA["rules"] = rules
        return DATA


# Define o schema
schema = Schema(query=Query)
