# convert_to_common.ps1
# Usage: cd "G:\myDrive\Docs\career-life\career-life-design" then .\convert_to_common.ps1

$SiteRoot = "G:\マイドライブ\Docs\career-life\career-life-design"
$Success = 0; $Skipped = 0; $Failed = 0

$files = Get-ChildItem -Path $SiteRoot -Recurse -Filter "*.html" |
         Where-Object { $_.FullName -notlike "*\.git\*" } |
         Sort-Object FullName

Write-Host "Target files: $($files.Count)"

foreach ($file in $files) {
    $rel = $file.FullName.Replace($SiteRoot + "\", "")
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)

    if ($content -match "common\.js") {
        Write-Host "  SKIP (done): $rel"
        $Skipped++
        continue
    }

    $changed = $false

    if ($content -notmatch "/assets/css/common\.css") {
        $content = $content -replace '<link rel="preconnect" href="https://fonts\.googleapis\.com">',
            "<link rel=`"stylesheet`" href=`"/assets/css/common.css`">`n<link rel=`"preconnect`" href=`"https://fonts.googleapis.com`">"
        $changed = $true
    }

    if ($content -match '<header class="site-header">') {
        $content = $content -replace '(?s)<header class="site-header">.*?</header>',
            '<div id="site-header"></div>'
        $changed = $true
    }

    if ($content -match '<footer class="site-footer">') {
        $content = $content -replace '(?s)<footer class="site-footer">.*?</footer>',
            '<div id="site-footer"></div>'
        $changed = $true
    }

    if ($content -notmatch "margin-top:60px" -and $content -notmatch "margin-top: 60px") {
        $content = $content -replace '<div class="page-hero">',
            '<div class="page-hero" style="margin-top:60px;">'
        $content = $content -replace '<nav class="breadcrumb">',
            '<nav class="breadcrumb" style="margin-top:60px;">'
        $changed = $true
    }

    if ($content -notmatch "/assets/js/common\.js") {
        $content = $content -replace '</body>',
            "<script src=`"/assets/js/common.js`"></script>`n</body>"
        $changed = $true
    }

    if ($changed) {
        $outBytes = [System.Text.Encoding]::UTF8.GetBytes($content)
        [System.IO.File]::WriteAllBytes($file.FullName, $outBytes)
        Write-Host "  OK: $rel"
        $Success++
    } else {
        Write-Host "  NO CHANGE: $rel"
        $Failed++
    }
}

Write-Host "Done: $Success converted / $Skipped skipped / $Failed no-change"
Write-Host "Next: git add . && git commit -m 'Add: common.js/css all pages' && git push origin main"
