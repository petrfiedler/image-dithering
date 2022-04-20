### _Moje průběžné poznámky a pozorování_

---

# Hledání nejbližší barvy:

-   lineární řešení pomalé

## Octree

-   při správné implementaci by mohlo zrychlit proces hledání
    nejbližší barvy
-   nad moje prozatimní algoritmické schopnosti (zasekl jsem se nad
    vyhledáváním podobných barev v oktantech, které nejsou ve stejné
    nadvětvi jako nejpřesnější vyplněný oktant - nutno použít prioritní
    frontu, víc nevím, na internetu je málo informací)

## Plány do budoucna

-   využít kd-tree ze scipy
-   po získání lepší znalosti numpy se pokusit alespoň lineární porovnávání
    zrychlit

# Výběr barevné palety:

## Median Cut

-   vybere nejreprezentativnější barvy
-   zanedbává barevné odstíny, které jsou na obrázku sice výrazné, ale
    nezabírají moc pixelů
-   vytváří hladký výsledek, ale zuniformní barvy
-   vhodný pro obrázky s jednolitým barevným odstínem bez výrazných
    barevných prvků

## Bit Stripping

-   pomalejší než median cut
-   lepší výsledky pro menší počet barev (nesmí být ale moc malé -
    ideální je strippovat 6 a méně bitů, případně vypnout kompenzaci
    ztráty, která například z bílé vytvoří fialovou při malé paletě)
-   zrnitější obraz, ale věrnější barvy
-   obecně lepší
-   doporučuji úroveň strippingu 5: vyprodukuje barevnou paletu o ~100
    barvách

## Plány do budoucna

-   výběr websafe barev
-   případně paleta rovnoměrně rozložených barev
-   hodně případně tvorba palety pomocí octree

# GUI:

## zobrazování obrázku

-   bylo nečekaně složité vytvořit zoom, který navíc správně zobrazuje pixely

## plány do budoucna

-   vytvořit classy, hlavně pro canvas, kde dočasně využívám globální proměnné
-   navíc to celé přepsat, zatím jsem napsal špagetový kód, jen aby to nějak fungovalo
-   pohybování obrázku
-   nastavení iniciální pozice na fit canvas
-   tmavý vzhled
-   zákaz moc zmenšeného okna
