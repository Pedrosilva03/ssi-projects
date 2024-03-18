# Respostas das Questões
## Q1
No arquivo MSG_SERVER.crt, a chave pública está contida. As informações extraídas revelam que a chave pública está a utilizar o algoritmo de criptografia rsaEncryption e tem um tamanho de 2048 bits. Além disso, o módulo (Modulus) e o expoente público (Exponent) foram especificados. O módulo é uma sequência hexadecimal longa que representa a base da operação de criptografia RSA, enquanto o expoente público é o valor padrão comumente usado para criptografia, neste caso, 65537 (0x10001).
No arquivo MSG_SERVER.key, a chave privada está armazenada. Novamente, é utilizada a criptografia RSA e o tamanho da chave é de 2048 bits. Além do módulo e do expoente público, também temos o expoente privado (Private Exponent), os primos (Prime1 e Prime2) que compõem o módulo, o expoente de D (Exponent1 e Exponent2) e o Coeficiente.
Ao comparar as informações da chave pública no certificado com as informações da chave privada, podemos ver que o módulo e o expoente público são os mesmos em ambas as chaves.
Portanto, com base nessas análises, podemos concluir que as informações fornecidas nos arquivos MSG_SERVER.crt e MSG_SERVER.key formam de fato um par de chaves RSA válido.

## Q2
Os campos do certificado que devem ser objeto de atenção no procedimento de virificação são:
1. Validade (Validity)
2. Algoritmo de Assinatura (Signature Algorithm)
3. Emissor (Issuer) e Sujeito (Subject)
4. Conteúdo da chave pública (Subject Public Key Info)
5. Extensões (Extensions)
6. Valor da Assinatura (Signature Value)
