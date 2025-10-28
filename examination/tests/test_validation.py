"""
filen ska stoppa felaktig indata och släppa igenom korrekt.
testområde:
datum saknas - fel
fel format - fel
datum före 2022 - 11 - 01 blir fel och datum i framtiden blir fel. Giltigt datum OK.

tickers:
inga tickers blir fel. fler än 10 Tickers blir fel. ogiltiga tecken blir fel.
blandade versaler är OK små/stor.
whitespace runt poster trimmas.

output:
valid True eller False . True om allting är godkänt. 
False om något var fel, exempelvis datum i framtiden.
errors - rätt felmeddelanden, om användaren lämnar en tom sträng på datum
så blir en error "Ange ett datum"
"""