$currPath = Get-Location
Write-Host $currPath

$argsCount = $args.Count

if(-not ($argsCount -eq 2)){
    Write-Host "Wrong Usage"
    Write-Host "Usage-> ./fim.ps1 [Folder to be monitered] [Options]"
    return
}

function LoadBaseline {
    param (
        $tbm,$baselinePath
    )
    $files = Get-ChildItem -Path $tbm
    "path,hash" | Out-File $baselinePath -Append
    foreach($file in $files){
        $hash = Get-FileHash -Path $file.FullName -Algorithm SHA512
        Write-Host $file.FullName
        "$($hash.Path),$($hash.Hash)" | Out-File $baselinePath -Append
    }

}



$tbm = $args[0]

# Write-Host "1)Create Baseline"
# Write-Host "2)Update Baseline"
# Write-Host "3)Start Monitoring"
$res = $args[1]

Write-Host $res

#creating baseline
if($res -eq 1){
    $baselinePath = Join-Path $currPath baseline.csv
    if(Test-Path -Path $baselinePath){
        Write-Host "Baseline Already Exists"
    }
    else {
        LoadBaseline $tbm $baselinePath
        Write-Host "Baseline Created"
    }
}

#updating baseline
elseif($res -eq 2){
    $baselinePath = Join-Path $currPath baseline.csv
    if(Test-Path -Path $baselinePath){
        Remove-Item -Path $baselinePath
        LoadBaseline $tbm $baselinePath
        Write-Host "Baseline Updated"
    }
    else {
        Write-Host "Baseline Doesnt Exist"
    }
}

#monitoring
elseif($res -eq 3){
    while ($true) {
        Start-Sleep -Seconds 1
        $baselinePath = Join-Path $currPath baseline.csv
        if(Test-Path -Path $baselinePath){
            $baselineFiles = Import-Csv -Path $baselinePath -Delimiter ','
            foreach($file in $baselineFiles){
                if(Test-Path -Path $file.path){
                    $tempHash = Get-FileHash -Path $file.Path -Algorithm SHA512

                    if($file.hash -eq $tempHash.Hash){

                    }
                    else{
                        Write-Host "The data of $($file.path) has been compromised"
                    }
                }
                else{
                    Write-Host "$($file.path) has been deleted or moved or renamed"
                }
            }
            
            $files = Get-ChildItem -Path $tbm
            foreach($file in $files){
                $existBool = $baselineFiles.path -contains $file.FullName
                if(-not $existBool){
                        Write-Host "A new file $($file) has been inserted"

                    
                }
            }
        }
        else {
            Write-Host "Baseline Doesn't Exist"
        }
        
    }
}


