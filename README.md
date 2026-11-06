# Modern Warfare Remastered – runtime FOV

Egyszerű, külső FOV-állító a **Call of Duty: Modern Warfare Remastered egyjátékos kampányához**. Az alapértelmezett látómező **105**, a megadható tartomány **65–110**.

## Követelmények

- Windows, **64 bites Python 3.9 vagy újabb**.
- Python-letöltés: [python.org – Windows](https://www.python.org/downloads/windows/). Telepítéskor engedélyezd a Python launchert (`py`), vagy add a Pythont a PATH-hoz. Telepítés után indítsd újra az indítót.
- Nincs szükség `pip install` parancsra vagy külső Python-csomagra.
- Rendszergazdai jóváhagyás: az eszköz induláskor UAC-engedélyt kér, hogy hozzáférjen a rendszergazdaként futó játékhoz.

**A mappa hordozható, de nem támogat automatikusan minden játékverziót.** A javító az alább megadott, ellenőrzött 1.3-as EXE-változatokkal működik. Más EXE-t elutasít; a verziószám önmagában nem elegendő.

## Telepítés és indítás

1. Töltsd le és csomagold ki a projektet. A `MWR FOV 105.cmd` és a `MWR-FOV.py` maradjon ugyanabban a mappában.
2. Tedd őket a `h1_sp64_ship.exe` mellé, vagy a játék könyvtárán belül egy almappába, például `fov` néven. Ebben az elrendezésben az indító a játékot is elindítja, ha még nem fut.
3. Más helyen is tarthatod a mappát. Ilyenkor előbb indítsd el a kampányt, majd az indítót; az eszköz a futó játékból határozza meg a játék könyvtárát.
4. Kattints duplán a `MWR FOV 105.cmd` fájlra, és engedélyezd a rendszergazdai indítást.
5. Tölts be egy pályát. A konzolban megjelennek a kiolvasott FOV-értékek. **A javító ablakát hagyd nyitva játék közben.**

Az indító a saját mappájából keresi a Python-fájlt, ezért parancssorból bármilyen aktuális könyvtárból elindítható. Nem tartalmaz felhasználóhoz vagy meghajtóhoz kötött telepítési útvonalat. A Python továbbra is szükséges minden gépen.

## Saját FOV beállítása

1. Jobb kattintás a `MWR FOV 105.cmd` fájlra → **Szerkesztés** (például Jegyzettömbbel).
2. Keresd meg ezt a sort:

   ```bat
   set "FOV=105"
   ```

3. Írd át a számot a kívánt értékre, például:

   ```bat
   set "FOV=90"
   ```

4. Mentsd el a fájlt. Ha a javító már fut, zárd be az ablakát, majd indítsd újra. A játékot ehhez nem kell újraindítani.

A nagyobb szám szélesebb látómezőt jelent. A megengedett tartomány **65–110**; azon kívüli értékkel az eszköz nem indul el. Egyszerre csak egy példány fusson. A CMD neve nem határozza meg a FOV-ot: átnevezheted például `MWR FOV.cmd` névre.

Parancssorból is megadható az érték:

```bat
py -3 "D:\Tools\fov\MWR-FOV.py" --fov 90
```

Ha a játék még nem fut, és a javító külön könyvtárban van:

```bat
py -3 "D:\Tools\fov\MWR-FOV.py" --fov 105 --game-dir "D:\Games\Call of Duty Modern Warfare Remastered"
```

Az asztali/parancsfájlos indító további argumentumokat is elfogad:

```bat
"D:\Tools\fov\MWR FOV 105.cmd" --fov 95 --game-dir "D:\Games\Call of Duty Modern Warfare Remastered"
```

## Mit módosít?

A javító a futó `h1_sp64_ship.exe` folyamatban megkeresi és ellenőrzi a `cg_fov` beállítást, majd annak aktuális, függőben lévő és visszaállítási értékét a választott FOV-ra állítja. Körülbelül 50 milliszekundumonként ellenőriz, és csak eltéréskor ír új értéket. Az írást visszaolvasással ellenőrzi.

**A runtime javító nem módosítja a lemezen lévő EXE-t vagy a játék konfigurációs fájljait.** Külön DLL/mod telepítése és az előző statikus EXE-patch nem szükséges hozzá. A tesztelt játékban a korábbi alapérték-módosítás önmagában nem volt elegendő; a futás közbeni FOV-állítás működött.

A konzol bezárása vagy a **Ctrl+C** leállítja az érték fenntartását; nem állítja rögtön vissza a korábbi FOV-ot. A játék teljes újraindítása törli a memóriabeli módosítást. Az eszköz a játék bezárásakor leáll.

Kizárólag az ellenőrzött **single-player kampányhoz** készült; multiplayerhez nincs támogatás. A projekt nem tartalmaz játékfájlokat, játék-EXE-t vagy DRM-módosítást.

## Támogatott EXE-k

Az ellenőrzött 1.3-as kiadás SHA-256 azonosítói:

| Változat | SHA-256 |
| --- | --- |
| A tesztelt telepítés módosítás előtti EXE-je | `f89c09864b88ef09bcceeebc1cdd7dcd19adeaf073ff464b1cc186e667f77cb5` |
| Ugyanez a korábbi, egybájtos 90-es alapérték-patch után | `d150b4414edcde81c9eed844ac232326d46cf4cd0ebb155506a80b3687b48702` |

A javító emellett ellenőrzi a memóriában lévő kódrészletet, a FOV-beállítás azonosítóját és típusát. Ismeretlen változat esetén nem ír a folyamat memóriájába. Nem általános megoldás minden Steam- vagy egyéb játékkiadáshoz.

## Hibaelhárítás

- **Python szükséges / nem található:** telepíts 64 bites Python 3.9+ verziót, a launcherrel vagy PATH-beállítással együtt.
- **Game process not found / a játék EXE-je nem található:** indítsd el előbb a kampányt, tedd a javítót a játék mellé vagy közvetlen almappájába, illetve használd a `--game-dir` kapcsolót.
- **Unsupported executable:** az EXE nem egyezik a két tesztelt változattal. Ne töröld a verzióellenőrzést: más verzióban eltérhetnek a memóriacímek.
- **Access denied:** engedélyezd az indító UAC-kérését, és ellenőrizd, hogy rendszergazdaként fut-e.
- **Nem látszik változás:** pályán ellenőrizd, ne csak a főmenüben. Nézd meg a konzolban a FOV-értékeket, és zárd be a többi FOV-állító példányt.

A diagnosztika a javító mappájában, a `FOV-runtime.log` fájlban található. Minden indítás felülírja. Hibajelentés előtt nézd át, mert tartalmazhatja a játék helyi elérési útját.

## Fejlesztői megjegyzés

A beállítás struktúrájának nyilvános referenciája: [Aurora H1-Mod – dvar_t](https://github.com/auroramod/h1-mod/blob/develop/src/client/game/structs.hpp). A folyamaton belüli címek a helyileg megvizsgált EXE-hez tartoznak. Más kiadás támogatásához külön vizsgálat és tesztelés szükséges.
