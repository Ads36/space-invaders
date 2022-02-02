# Space invaders od Adama Červenky
## Zadání
Hra v Pythonu podobná původním Space invaders vytvořená za pomoci knihovny pygame. Ve hře ovládáme raketu, která střílí po nepřátelích. Nepřátelé ale shazují bomby, které mohou raketu zničit. 
Cíl hry je sestřelit co nejvíce nepřátel a nenechat se přitom zasáhnout bombou nebo nepřítelem.
Hra končí, když je raketa zasažena bombou nebo nepřítel dosáhne vertikální úrovně rakety.

## Ovládání
Raketa se pohybuje stiskem kláves šipka doleva a šipka doprava nebo „a“ a „d“ (kombinace je možná, ale nedoporučovaná). Střela se vystřelí stiskem mezerníku. Po skončení hry je možný restart také stiskem mezerníku. Vypnutí hry je standardně klikem na křížek.

## Zvolený algoritmus
Žádný speciální složitý algoritmus jsem nepoužil. V programu jsou všechny algoritmy okomentovány.

## Program
Program je přirozeně rozdělen na 3 části. První část je inicializační, probíhá zde nastavování okna pro hru, vytváření konstant a určitých globálních proměnných. Druhá část se týká různých funkcí. V programu jsou funkce na vykreslování herních objektů, funkce na řešení kolizí herních objektů, funkce na provádění akcí s herními objekty a funkce na konec hry. Třetí část programu je samotný while cyklus ve kterém běží hra. V této části je jediný uživatelský vstup do programu, a to reagování na stisk určitých kláves. Zde také probíhá volání funkcí na vykreslování a na provádění akcí. 

V inicializační části jsem nastavil velikost okna, pozadí, ikonku, importoval použité knihovny, připravil texty, hodiny, barvy, definoval konstanty a další proměnné (pro raketu, střelu).

V části týkající se funkcí jsem napsal funkce na vykreslování všech herních objektů, vytvoření nových nepřátel, bomb, přidání bomby, kolizí, konce hry a akce bomb, nepřátel a střely.
Nepřátele jsem reprezentoval pomocí 4 polí délky počtu nepřátel: obrázky, pozice X, pozice Y a rychlost. 
Raketu (hráče) jsem reprezentoval pomocí proměnných na x-ovou a y-ovou souřadnici. Raketa je jediný prvek hry, který hráč může ovládat. 
Bomby jsou reprezentované x-ovou a y-ovou souřadnicí a také. Bomby dropují, pokud vygenerované náhodné číslo patří do určitého intervalu. Vychytávka: bomby mají větší šanci, že spadnou, pokud nepřítel je přímo nad raketou – tímto je hráč donucen hýbat se.
Střelu jsem reprezentoval x-ovou a y-ovou souřadnicí a booleanem jestli je vystřeleno nebo ne.

Pomocí pozicování x-ových a y-ových souřadnic jsem kontroloval kolize ve funkcích enemy_bullet_collision a rocket_bomb_collision. Po kolizi střely a nepřítele se nepřítel znovu spawne s náhodnými souřadnicemi, čili celkový počet nepřátel ve hře zůstává stejný (kvůli zachování obtížnosti). Po kolizi rakety a bomby hra končí.

Ve třetí části (ve while cyklu) už je pouze cyklus na zjišťování stisku kláves (viz ovládání), změna pohybu rakety, volání funkcí pro akce s herními objekty, clock tick a update okna.

__Obtížnost__ hry se nechá snadno upravovat pomocí změny konstant a globálních proměnných. 
Všechny __obrázky__ ze hry jsou __volně dostupné__ bez licence (pixabay.com) a jsou upraveny.

## Alternativní programové řešení
Bomby by mohly být sestřeleny střelou z rakety. Počet nepřátel by se mohl lineárně zvyšovat s délkou jedné hry.  

## Reprezentace vstupních dat
Vstupní data jsou pouze stisky kláves a klik na křížek popsané v ovládání, uživatel vstupem nemůže nic pokazit. 

## Reprezentace výstupních dat
Jediný výstup programu je dění na obrazovce a po skončení hry zobrazení maximálního skóre. 

## Průběh práce
Hru jsem původně chtěl vytvořit o Vánočních prázdninách, ale byl jsem moc líný :D. Tak jsem jí zvládl napsat za zhruba 4 dny po všech zkouškách na konci zkouškového období. Díky psaní programu jsem se naučil aspoň trochu pracovat s gitem, i když moje commitování a postování má ještě nějaké mouchy.

## Co nebylo doděláno
Myslím, že vše, co jsem si zadal za cíl vytvořit, se mi povedlo. Případné další možné dodělávky jsem uvedl v alternativních programových řešeních.

Sada testovacích příkladů není v tomto programu možná, nejlepší otestování si udělá hráč hraním.

## Závěrem
Tvorba programu byla v pohodě, bavilo mě to a těším se na příští semestr a pokračování studia na MFF!
