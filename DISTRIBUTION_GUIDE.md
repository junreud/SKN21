# 🃏 솔리테리 게임 배포 가이드

이 가이드는 솔리테리 게임을 Windows(.exe)와 macOS(.app) 실행 파일로 만들어 배포하는 방법을 설명합니다.

## 🎯 목표
- **Windows**: `Solitaire.exe` - 더블클릭으로 바로 실행
- **macOS**: `Solitaire.app` - 응용 프로그램으로 설치 가능
- **사용자**: Python 설치 없이도 게임 즐기기 가능

## 🛠️ 빌드 과정

### 1단계: 환경 준비
```bash
# 1. Python 3.7+ 설치 확인
python3 --version

# 2. 프로젝트 폴더로 이동
cd /path/to/solitaire-project

# 3. 가상환경 생성 (첫 번째 실행시만)
python3 -m venv solitaire_env
```

### 2단계: 의존성 설치
```bash
# 가상환경 활성화
# macOS/Linux:
source solitaire_env/bin/activate
# Windows:
solitaire_env\Scripts\activate.bat

# 필요한 패키지 설치
pip install pygame==2.6.1 pyinstaller==6.16.0
```

### 3단계: 실행 파일 생성

#### 🍎 macOS 빌드
```bash
# 자동 빌드 (권장)
chmod +x build.sh
./build.sh

# 수동 빌드
pyinstaller --onedir --windowed --name "Solitaire" solitaire_pygame.py
```

**결과**: `dist/Solitaire.app` (약 20-25MB)

#### 🪟 Windows 빌드
```cmd
REM 자동 빌드 (권장)
build_windows.bat

REM 수동 빌드
pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py
```

**결과**: `dist/Solitaire.exe` (약 15-20MB)

## 📦 배포 파일 구조

빌드 완료 후 `dist` 폴더 구조:
```
dist/
├── Solitaire.app/          # macOS 응용프로그램 번들
│   └── Contents/
│       ├── Info.plist
│       ├── MacOS/
│       │   └── Solitaire   # 실행파일
│       └── Resources/
└── Solitaire.exe           # Windows 실행파일 (onefile 모드시)
```

## 🚀 배포 방법

### Windows 사용자에게 배포
1. `dist/Solitaire.exe` 파일을 복사
2. 사용자에게 전달 (이메일, USB, 다운로드 등)
3. 사용자는 더블클릭으로 바로 실행
4. **필요한 것**: 없음! (Python 설치 불필요)

### macOS 사용자에게 배포
1. `dist/Solitaire.app`을 압축: `zip -r Solitaire.zip Solitaire.app`
2. 사용자에게 압축파일 전달
3. 사용자는 압축 해제 후 응용 프로그램 폴더로 이동
4. Launchpad 또는 Finder에서 실행

### DMG 생성 (macOS만, 선택사항)
```bash
# DMG 인스톨러 생성
hdiutil create -volname "Solitaire Game" -srcfolder dist/Solitaire.app -ov -format UDZO dist/Solitaire.dmg
```

## 🔧 고급 설정

### 아이콘 추가
1. **Windows**: `.ico` 파일 준비
2. **macOS**: `.icns` 파일 준비
3. 빌드 명령에 아이콘 옵션 추가:
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name "Solitaire" solitaire_pygame.py
```

### 최적화 옵션
```bash
# 더 작은 파일 크기
pyinstaller --onefile --windowed --strip --upx-dir=/path/to/upx

# 콘솔 창 숨기기 (이미 적용됨)
pyinstaller --windowed

# 디버그 정보 제거
pyinstaller --strip
```

## 📊 파일 크기 최적화

| 옵션 | Windows | macOS | 설명 |
|------|---------|-------|------|
| 기본 | 15-20MB | 20-25MB | 표준 빌드 |
| --strip | 12-18MB | 18-23MB | 디버그 정보 제거 |
| UPX 압축 | 8-15MB | 15-20MB | 실행파일 압축 |

## ✅ 테스트 체크리스트

배포 전 확인사항:
- [ ] 게임이 정상 실행됨
- [ ] 카드 이동 기능 동작
- [ ] 새 게임 버튼 작동
- [ ] 승리 조건 확인
- [ ] 창 크기 적절함
- [ ] 다른 컴퓨터에서 실행 테스트

## 🎮 게임 기능 소개

사용자에게 소개할 게임 기능:
- ✨ **클래식 솔리테리**: 전통적인 클론다이크 규칙
- 🎨 **아름다운 그래픽**: 깔끔하고 컬러풀한 인터페이스
- 🖱️ **간편한 조작**: 클릭 앤 드래그로 카드 이동
- 🏆 **승리 조건**: 4개 파운데이션 완성시 승리
- 🔄 **새 게임**: 언제든 새로운 게임 시작
- 📱 **반응형**: 다양한 화면 크기 지원

## 🐛 문제 해결

### 빌드 에러
1. **ModuleNotFoundError**: `pip install pygame pyinstaller` 재실행
2. **Permission denied**: `chmod +x build.sh` 실행
3. **가상환경 활성화 실패**: 경로 확인 후 다시 생성

### 실행 에러
1. **Windows Defender 경고**: 안전한 파일로 예외 처리
2. **macOS 보안 경고**: 시스템 환경설정 > 보안 > "확인되지 않은 개발자" 허용
3. **파일 실행 안됨**: 실행 권한 확인 (`chmod +x`)

## 📝 라이센스 고려사항

배포시 포함할 정보:
- 게임 버전 정보
- 개발자 크레딧
- 사용된 라이브러리 (pygame) 라이센스
- 연락처 정보 (선택사항)

---

**🎉 축하합니다!** 이제 여러분의 솔리테리 게임을 전 세계와 공유할 수 있습니다!