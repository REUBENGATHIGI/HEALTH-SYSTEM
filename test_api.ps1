# 1. Test Program Creation
$programData = @{
    name = "Diabetes Care"
    description = "Blood sugar management program"
} | ConvertTo-Json

try {
    $program = Invoke-RestMethod -Uri "http://localhost:5000/api/programs" -Method Post -Body $programData -ContentType "application/json"
    Write-Host "✅ Program created successfully:" -ForegroundColor Green
    $program | Format-List
}
catch {
    Write-Host "❌ Failed to create program:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit
}

# 2. Verify Program Exists
try {
    $programs = Invoke-RestMethod -Uri "http://localhost:5000/api/programs"
    Write-Host "`n📋 Current Programs:" -ForegroundColor Cyan
    $programs | Format-Table -AutoSize
}
catch {
    Write-Host "❌ Failed to fetch programs:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

# 3. Create Client
$clientData = @{
    name = "John Doe"
    email = "john@example.com"
} | ConvertTo-Json

try {
    $client = Invoke-RestMethod -Uri "http://localhost:5000/api/clients" -Method Post -Body $clientData -ContentType "application/json"
    Write-Host "`n✅ Client registered successfully:" -ForegroundColor Green
    $client | Format-List
}
catch {
    Write-Host "❌ Failed to register client:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit
}

# 4. Enroll Client
$enrollmentData = @{
    program_id = 1
} | ConvertTo-Json

try {
    $enrollment = Invoke-RestMethod -Uri "http://localhost:5000/api/clients/1/enroll" -Method Post -Body $enrollmentData -ContentType "application/json"
    Write-Host "`n✅ Enrollment successful:" -ForegroundColor Green
    $enrollment | Format-List
}
catch {
    Write-Host "❌ Failed to enroll client:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit
}

# 5. Final Verification
try {
    $clientDetails = Invoke-RestMethod -Uri "http://localhost:5000/api/clients/1"
    Write-Host "`n🔍 Client Details:" -ForegroundColor Cyan
    $clientDetails | Format-List
}
catch {
    Write-Host "❌ Failed to get client details:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

Write-Host "`nTest sequence completed" -ForegroundColor Yellow