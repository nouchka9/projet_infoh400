# 📖 Complete User Guide - HL7 Messenger v1.0

## 🏥 System Overview

**HL7 Messenger** is a comprehensive hospital messaging solution developed to facilitate standardized communication between hospital departments. This production-ready application implements the HL7 v2.5 standard with the MLLP transport protocol to ensure secure and reliable exchanges.

### 🎯 **System Objectives**
- **Standardization**: HL7 v2.5 communication compliant with international standards
- **Interoperability**: Seamless exchanges between hospital departments
- **Reliability**: Robust architecture with complete error handling
- **Simplicity**: Intuitive interface for non-technical users
- **Traceability**: Complete history of messages and patients

### 🏥 **Supported Departments**
- **🏥 Admission**: Patient registration and management
- **🔬 Laboratory**: Transmission of analysis results
- **📡 Radiology**: Examination orders and imaging results
- **💊 Pharmacy**: Prescription management

---

## 🚀 Installation and Configuration

### 📋 **System Requirements**

#### Minimum Configuration
- **Operating System**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB available
- **Network**: TCP ports 2575-2579 available

#### Environment Verification
```bash
# Check Python version
python --version
# Should display: Python 3.8.x or higher

# Check pip
pip --version

# Check available ports (Linux/macOS)
netstat -an | grep 2575
# No result = port available
```

### 📦 **Dependency Installation**

#### Standard Installation
```bash
# Navigate to project folder
cd hl7_messenger

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python validate_fixes.py
```

#### Main Dependencies
- **hl7apy**: Official HL7 library for Python
- **tkinter**: Graphical interface (included with Python)
- **threading**: Multi-client management (standard Python)
- **json**: Data persistence (standard Python)
- **socket**: Network communication (standard Python)

### ⚙️ **System Configuration**

#### Network Configuration (`app/config.py`)
```python
# Main server configuration
MLLP_SERVER_HOST = "0.0.0.0"      # Listen on all interfaces
MLLP_SERVER_PORT = 2575            # Main HL7 port

# Destinations by department
DESTINATIONS = {
    "ADMISSION_SYSTEM": {"host": "localhost", "port": 2575},
    "LAB_SYSTEM": {"host": "localhost", "port": 2575},
    "ORDER_SYSTEM": {"host": "localhost", "port": 2575},
    "PHARMACY_SYSTEM": {"host": "localhost", "port": 2575}
}

# Communication parameters
TIMEOUT = 30                       # Network timeout in seconds
MAX_MESSAGE_SIZE = 1048576         # Maximum message size (1MB)
BUFFER_SIZE = 4096                 # Reception buffer size
```

#### Authentication Configuration (`app/utils/security.py`)
```python
# Default user accounts
DEFAULT_USERS = {
    "admin": {"password": "password", "role": "administrator"},
    "anouchka": {"password": "libre", "role": "admission"},
    "christelle": {"password": "456", "role": "laboratory"},
    "romeo": {"password": "789", "role": "radiology"},
    "calixta": {"password": "abc", "role": "pharmacy"}
}
```

---

## 🎮 System Startup

### 🖥️ **Launch Methods**

#### Method 1: Quick Start (Recommended)
```bash
# Terminal 1: HL7 Server (mandatory)
python app/network/mllp_server.py

# Terminal 2: User Interface
python run_app.py
```

#### Method 2: Classic Startup
```bash
# Terminal 1: HL7 Server
python -m app.network.mllp_server

# Terminal 2: Main Application
python app/main.py
```

#### Method 3: Startup with Validation
```bash
# Complete validation then launch
python validate_fixes.py && python run_app.py
```

### 🔍 **Startup Verification**

#### HL7 Server Started Correctly
```
🏥 HL7 MLLP Server Initialized
📍 Address: 0.0.0.0:2575
📚 Database: ✅ Available
🚀 Starting HL7 server...
✅ Socket bound on 0.0.0.0:2575
===============================================
🎉 HL7 SERVER STARTED SUCCESSFULLY!
🌐 Listening on 0.0.0.0:2575
⏰ Started on 29/05/2025 at 19:15:32
📨 Waiting for HL7 messages...
===============================================
```

#### Application Started Correctly
```
🚀 Initializing HL7 Messenger...
✅ Configuration loaded
✅ Database initialized
✅ User interface ready
📱 Application started successfully
```

---

## 🔐 Authentication and Navigation

### 🚪 **Login Screen**

#### Login Interface
The login screen presents three main fields:
- **👤 Username**: User identifier
- **🔒 Password**: Associated password
- **🏥 Department**: Hospital service assignment

#### Default Accounts
| Username | Password | Department | Role |
|----------|----------|------------|------|
| `admin` | `password` | All | Administrator |
| `anouchka` | `libre` | ADMISSION | Admission Manager |
| `christelle` | `456` | LABORATORY | Lab Technician |
| `romeo` | `789` | RADIOLOGY | Radiology Technician |
| `calixta` | `abc` | PHARMACY | Pharmacist |

#### Keyboard Navigation
- **Tab**: Move to next field
- **Shift+Tab**: Return to previous field
- **Enter**: Validate login
- **Escape**: Clear all fields

### 🏠 **Main Dashboard**

#### Overview
The central dashboard displays:
- **📊 Real-time Statistics**: Number of messages sent/received
- **🔗 Connection Status**: Server and MLLP client status
- **👥 Active Patients**: List of recently processed patients
- **📈 Recent Activity**: History of recent actions

#### Available Features
- **🏥 Department Access**: Buttons for each service
- **📜 Complete History**: Message exchange consultation
- **⚙️ Configuration**: System and network settings
- **🔌 Connection Testing**: Communication diagnostics
- **📊 Reports**: Usage statistics generation

---

## 🏥 Department Guide

### 🏥 **Admission Module**

#### Main Features
The admission module enables complete management of incoming patients:
- **New patient registration** with complete validation
- **Inter-service transfers** with traceability
- **Existing patient record updates**
- **Scheduled discharges** with notifications
- **ADT message generation** compliant with HL7 v2.5

#### User Interface

##### Patient Form (mandatory fields marked with *)
```
📋 Patient Information
┌─────────────────────────────────────────────────────────┐
│ 🆔 Patient ID *     : [P12345    ] 👤 Last Name * : [DOE    ]│
│ 👤 First Name *     : [JOHN      ] 📅 Birth Date : [19800101]│
│ ⚧ Gender           : [M ▼]        🏢 Service     : [CARDIO  ]│
│ 🛏️ Room             : [102       ] 👨‍⚕️ Doctor      : [Dr.MARTIN]│
│ 📨 Message Type    : [ADT^A01 - Admission ▼]              │
│ 📝 Comments        : [Scheduled admission               ] │
└─────────────────────────────────────────────────────────┘
[🔄 Reset] [🚀 Send Message] ✅ Ready
```

##### Supported ADT Message Types
- **ADT^A01**: Patient admission
- **ADT^A02**: Patient transfer
- **ADT^A03**: Patient discharge
- **ADT^A04**: Patient registration
- **ADT^A08**: Information update

##### Data Validation
- **Patient ID**: Minimum 2 characters, unique
- **Last/First Name**: Minimum 2 characters, alphabetic format
- **Birth Date**: YYYYMMDD format (e.g., 19800101)
- **Gender**: M (Male), F (Female), O (Other), U (Unknown)
- **Service**: Hospital service code
- **Room**: Available room number

#### Usage Workflow
1. **Enter patient information** in the form
2. **Real-time validation** of mandatory fields
3. **Select appropriate** ADT message type
4. **Add comments** if necessary
5. **Send message** to admission system
6. **Receive ACK** confirmation
7. **Automatic save** of patient to database

#### Generated HL7 Messages
```
MSH|^~\&|HL7MESSENGER|HOSPITAL|ADT|HOSPITAL|20250529191532||ADT^A01|12345|P|2.5
EVN||20250529191532
PID|1||P12345||DOE^JOHN||19800101|M
PV1|1|I|CARDIO^102||||||||||||||20250529191532
```

### 🔬 **Laboratory Module**

#### Main Features
The laboratory module manages transmission of analysis results:
- **Multi-parameter biological results**
- **Standardized LOINC codes**
- **Reference values** with anomalies
- **Detailed technical comments**
- **ORU message generation** compliant with HL7 v2.5

#### User Interface

##### Laboratory Results Form
```
🔬 Laboratory Results
┌─────────────────────────────────────────────────────────┐
│ 👤 Patient ID *     : [P12345    ] 📋 Request ID : [LAB001 ]│
│ 🧪 Exam Code *      : [GLU       ] 📝 Exam Name  : [Glucose]│
│ 📅 Exam Date       : [20250529  ] ⏰ Time       : [14:30  ]│
│                                                           │
│ 📊 Result 1                                              │
│ 🔬 Test Code       : [GLU       ] 📝 Test Name  : [Glucose]│
│ 📈 Value           : [95        ] 📏 Unit       : [mg/dL  ]│
│ 📊 Reference       : [70-110    ] ⚠️ Anomaly    : [Normal ]│
│                                                           │
│ 📊 Result 2 (optional)                                   │
│ 🔬 Test Code       : [HBA1C     ] 📝 Test Name  : [HbA1c  ]│
│ 📈 Value           : [5.8       ] 📏 Unit       : [%      ]│
│ 📊 Reference       : [<6.5      ] ⚠️ Anomaly    : [Normal ]│
│                                                           │
│ 📝 Comments        : [Results within normal range       ] │
└─────────────────────────────────────────────────────────┘
[🔄 Reset] [🚀 Send Results] ✅ Ready
```

##### Anomaly Codes
- **N**: Normal (within limits)
- **H**: High (above normal)
- **L**: Low (below normal)
- **HH**: Critically high
- **LL**: Critically low
- **A**: Abnormal (unspecified)

#### Usage Workflow
1. **Receive analysis request** from physician
2. **Perform examinations** in laboratory
3. **Enter results** in interface
4. **Biological validation** by technician
5. **Send results** to patient record
6. **Notify prescribing** physician
7. **Archive results** in database

#### Generated HL7 Messages
```
MSH|^~\&|HL7MESSENGER|HOSPITAL|LAB|HOSPITAL|20250529143000||ORU^R01|LAB001|P|2.5
PID|1||P12345
OBR|1|LAB001||GLU^Glucose|||20250529143000
OBX|1|NM|GLU^Glucose|95|mg/dL|70-110|N||F||20250529143000
OBX|2|NM|HBA1C^HbA1c|5.8|%|<6.5|N||F||20250529143000
```

### 📡 **Radiology Module**

#### Main Features
The radiology module covers two aspects:
- **Examination orders** (ORM^O01) for planning
- **Imaging results** (ORU^R01) with reports
- **Priority management** and emergencies
- **Complete examination workflow** tracking

#### Examination Orders Interface
```
📡 Radiology Examination Orders
┌─────────────────────────────────────────────────────────┐
│ 👤 Patient ID *     : [P12345    ] 📋 Order ID   : [RX001 ]│
│ 🔬 Exam Code *      : [CHEST     ] 📝 Exam Name  : [Chest X-ray]│
│ 📅 Scheduled Date   : [20250530  ] ⏰ Time       : [09:00  ]│
│ ⚡ Priority         : [ROUTINE ▼] 📍 Location    : [Room 1 ]│
│ 👨‍⚕️ Ordering Doctor : [Dr.MARTIN ] 🎯 Indication : [Persistent cough]│
│ 📝 Comments        : [Claustrophobic patient - consider sedation]│
└─────────────────────────────────────────────────────────┘
[🔄 Reset] [🚀 Schedule Exam] ✅ Ready
```

#### Examination Results Interface
```
📡 Radiology Examination Results
┌─────────────────────────────────────────────────────────┐
│ 👤 Patient ID *     : [P12345    ] 📋 Exam ID    : [RX001 ]│
│ 🔬 Exam Code *      : [CHEST     ] 📝 Exam Name  : [Chest X-ray]│
│ 📅 Performed Date   : [20250530  ] ⏰ Time       : [09:15  ]│
│ 👨‍⚕️ Radiologist     : [Dr.DUPONT ] 📊 Status     : [FINAL ▼]│
│                                                           │
│ 📋 Report                                                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ TECHNIQUE:                                          │ │
│ │ Frontal and lateral chest radiography              │ │
│ │                                                     │ │
│ │ RESULTS:                                            │ │
│ │ - Well-expanded lungs                               │ │
│ │ - No parenchymal opacity                           │ │
│ │ - Normal cardiac silhouette                        │ │
│ │ - Free diaphragmatic domes                         │ │
│ │                                                     │ │
│ │ CONCLUSION:                                         │ │
│ │ Normal chest examination                           │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
[🔄 Reset] [🚀 Send Results] ✅ Ready
```

#### Supported Examination Types
- **CHEST**: Chest radiography
- **ABDO**: Abdominal radiography
- **SKULL**: Skull radiography
- **ECHO**: Ultrasound
- **SCAN**: CT scan
- **MRI**: Magnetic resonance imaging
- **MAMMO**: Mammography

#### Usage Workflow
1. **Receive medical** prescription
2. **Schedule examination** with time slots
3. **Patient preparation** if necessary
4. **Perform examination** by technician
5. **Image interpretation** by radiologist
6. **Write detailed** report
7. **Final validation** and send results

### 💊 **Pharmacy Module**

#### Main Features
The pharmacy module manages medication prescriptions:
- **Multi-medication prescriptions** (up to 2 per prescription)
- **Detailed dosages** with frequencies
- **Drug interaction** verification
- **Special instructions** for patient
- **ORM message generation** for dispensing

#### User Interface
```
💊 Medication Prescriptions
┌─────────────────────────────────────────────────────────┐
│ 👤 Patient ID *     : [P12345    ] 📋 Prescription ID: [RX001]│
│ 👨‍⚕️ Doctor *        : [Dr.MARTIN ] 📅 Prescription Date: [20250529]│
│                                                           │
│ 💊 Medication 1                                          │
│ 🔢 Drug Code        : [PARA500   ] 📝 Brand Name : [Doliprane]│
│ 💉 Dosage          : [500mg     ] 📊 Form       : [Tablet ▼]│
│ ⏰ Dosing          : [1 tab x 3/d] 🔄 Duration   : [7 days ]│
│ 📝 Instructions    : [Take with meals]                   │
│                                                           │
│ 💊 Medication 2 (optional)                               │
│ 🔢 Drug Code        : [AMOX1000  ] 📝 Brand Name : [Amoxicillin]│
│ 💉 Dosage          : [1000mg    ] 📊 Form       : [Tablet ▼]│
│ ⏰ Dosing          : [1 tab x 2/d] 🔄 Duration   : [10 days]│
│ 📝 Instructions    : [Complete full course of treatment] │
│                                                           │
│ 📝 Comments        : [Check penicillin allergy]         │
└─────────────────────────────────────────────────────────┘
[🔄 Reset] [🚀 Send Prescription] ✅ Ready
```

#### Pharmaceutical Forms
- **Tablet**: Standard solid form
- **Capsule**: Encapsulated form
- **Syrup**: Oral liquid form
- **Solution**: Injectable liquid form
- **Ointment**: Topical form
- **Suppository**: Rectal form
- **Patch**: Transdermal form

#### Usage Workflow
1. **Receive medical** prescription
2. **Check medication** availability
3. **Control interactions** and contraindications
4. **Prepare pill organizer** if necessary
5. **Label detailed** dosing
6. **Dispense to patient** with counseling
7. **Follow adherence** for long-term treatment

---

## 📊 Data Management and History

### 💾 **Patient Database**

#### Patient Data Structure
```json
{
    "id": "P12345",
    "personal_info": {
        "last_name": "DOE",
        "first_name": "JOHN", 
        "birth_date": "19800101",
        "gender": "M"
    },
    "hospital_info": {
        "ward": "CARDIO",
        "room": "102",
        "attending_doctor": "Dr.MARTIN",
        "admission_date": "20250529191532"
    },
    "contact_info": {
        "phone": "+32123456789",
        "address": "123 Health Street, 1000 Brussels",
        "emergency_contact": "Jane DOE - Wife"
    },
    "medical_info": {
        "allergies": ["Penicillin"],
        "medical_history": ["Hypertension", "Type 2 Diabetes"],
        "current_medications": ["Metformin 850mg", "Amlodipine 5mg"]
    },
    "metadata": {
        "created_date": "20250529191532",
        "last_updated": "20250529191532",
        "created_by": "anouchka",
        "total_visits": 3
    }
}
```

#### Storage File
- **Location**: `resources/patients.json`
- **Format**: Structured JSON with automatic validation
- **Backup**: Automatic after each modification
- **Backup**: Timestamped copies in `backup_*/`

### 📨 **Message History**

#### HL7 Message Structure
```json
{
    "id": "msg_12345678-1234-5678-9abc-123456789abc",
    "message_info": {
        "type": "ADT^A01",
        "control_id": "20250529-12345",
        "timestamp": "20250529191532",
        "status": "SENT_SUCCESS"
    },
    "communication": {
        "source": "HL7MESSENGER",
        "destination": "ADMISSION_SYSTEM", 
        "source_ip": "127.0.0.1:54321",
        "destination_ip": "127.0.0.1:2575"
    },
    "patient_ref": {
        "patient_id": "P12345",
        "patient_name": "DOE^JOHN"
    },
    "content": {
        "raw_message": "MSH|^~\\&|HL7MESSENGER|...",
        "parsed_segments": {
            "MSH": {...},
            "PID": {...},
            "PV1": {...}
        }
    },
    "acknowledgment": {
        "ack_received": true,
        "ack_code": "AA",
        "ack_message": "Message processed successfully",
        "ack_timestamp": "20250529191533"
    }
}
```

### 📈 **History Interface**

#### Consultation Features
```
📜 HL7 Message History
┌─────────────────────────────────────────────────────────┐
│ 🔍 Filters                                              │
│ 📅 From: [29/05/2025] To: [29/05/2025] 📨 Type: [All ▼]│
│ 👤 Patient: [All     ] 🏥 Department: [All       ▼] │
│ 📊 Status: [All     ▼] 🔄 [Apply Filters]             │
│                                                         │
│ 📋 Messages (25 results)                               │
│ ┌─────────────────────────────────────────────────────┐ │
│ │19:15:32│ADT^A01│P12345│DOE JOHN    │✅ Sent        │ │
│ │19:12:15│ORU^R01│P12344│SMITH JANE  │✅ Sent        │ │
│ │19:08:45│ORM^O01│P12343│MARTIN PAUL │❌ Error       │ │
│ │19:05:22│ADT^A02│P12342│BROWN MARY  │✅ Sent        │ │
│ │18:58:11│ORU^R01│P12341│WILSON TOM  │✅ Sent        │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [📄 Export CSV] [🔍 Details] [🔄 Refresh]             │
└─────────────────────────────────────────────────────────┘
```

#### Export Options
- **CSV**: Excel file for analysis
- **PDF**: Formatted report for printing
- **JSON**: Raw data for integration
- **HL7**: Raw messages for debugging

---

## 🌐 Network Communication and Protocols

### 📡 **Network Architecture**

#### Communication Schema
```
┌─────────────────┐    MLLP/TCP     ┌─────────────────┐
│  UI Interface   │ ─────────────► │  HL7 Server     │
│  (Departments)  │                │  (Port 2575)    │
└─────────────────┘                └─────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                ┌─────────────────┐
│  MLLP Client    │                │ MLLP Reception  │
│  (Send)         │                │ (Multi-client)  │
└─────────────────┘                └─────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                ┌─────────────────┐
│ HL7 Message     │◄──── ACK ──────│  HL7 Parser     │
│ (ADT/ORU/ORM)   │                │  (Validation)   │
└─────────────────┘                └─────────────────┘
                                            │
                                            ▼
                                  ┌─────────────────┐
                                  │ Database        │
                                  │ (JSON Storage)  │
                                  └─────────────────┘
```

### 🔌 **MLLP Protocol**

#### MLLP Message Structure
```
[SB] + [HL7 Message] + [EB] + [CR]
 ↓         ↓           ↓       ↓
0x0B   HL7 Content   0x1C    0x0D
```

#### Complete Example
```
Hexadecimal: 0B 4D 53 48 7C ... 1C 0D
ASCII      : [SB]MSH|^~\&|HL7MESSENGER|...[EB][CR]
```

#### ACK Management
```python
# Success ACK
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK^ADT^A01|12345|P|2.5
MSA|AA|12345|Message processed successfully

# Application error ACK  
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK|12345|P|2.5
MSA|AE|12345|Error: Patient does not exist

# Rejection ACK
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK|12345|P|2.5
MSA|AR|12345|Message rejected: Invalid format
```

### 🔍 **Quick System Test**

#### Connection and Basic Test
1. **Start server**: `python app/network/mllp_server.py`
2. **Launch application**: `python run_app.py`
3. **Connect**: 
   - Username: `anouchka`
   - Password: `libre`
   - Department: `ADMISSION`
4. **Test sending** an ADT^A01 message
5. **Verify reception** in server logs
6. **Confirm storage** of patient in database

#### Ready-to-use Test Data
Forms are pre-filled with valid test data:
- **Patient**: P12345 - DOE JOHN
- **Service**: CARDIO, Room 102
- **Doctor**: Dr. MARTIN
- **Date**: Automatically today

## 🔧 Advanced Configuration

### Performance Parameters
```python
# Production-optimized configuration (config.py)
PERFORMANCE_SETTINGS = {
    "max_concurrent_clients": 50,      # Max simultaneous clients
    "thread_pool_size": 10,            # Server thread pool
    "message_queue_size": 100,         # Message queue size
    "connection_timeout": 30,          # Connection timeout (sec)
    "keep_alive_interval": 60,         # Keep-alive interval (sec)
    "max_message_size": 1048576,       # Max message size (1MB)
    "buffer_size": 8192,               # Network buffer size
    "enable_compression": False,        # Message compression (future)
    "log_level": "INFO"                # Logging level
}
```

### Multi-site Configuration
```python
# Remote site support (config_multisite.py)
REMOTE_SITES = {
    "central_site": {
        "host": "10.1.1.100",
        "port": 2575,
        "description": "Central Hospital"
    },
    "emergency_site": {
        "host": "10.1.2.100", 
        "port": 2575,
        "description": "Emergency Service"
    },
    "pediatric_site": {
        "host": "10.1.3.100",
        "port": 2575,
        "description": "Pediatric Hospital"
    }
}
```

## 🔍 Diagnostics and Troubleshooting

### 🚨 Common Problems and Solutions

#### Problem 1: Server Won't Start
**Symptoms:**
```
❌ Error: Port 2575 already in use
OSError: [Errno 48] Address already in use
```

**Solutions:**
```bash
# Check processes using the port
lsof -i :2575
netstat -an | grep 2575

# Kill process using the port
sudo kill -9 [PID]

# Or use another port
python app/network/mllp_server.py 2580
```

#### Problem 2: Client Cannot Connect
**Symptoms:**
```
❌ Connection refused by localhost:2575
ConnectionRefusedError: Connection refused
```

**Solutions:**
1. Verify server is started
```bash
ps aux | grep mllp_server
```

2. Test connectivity
```bash
telnet localhost 2575
# Should display: Connected to localhost
```

3. Check server logs
```bash
tail -f logs/hl7_messenger.log
```

#### Problem 3: Messages Not Received
**Symptoms:**
- Interface shows "✅ Send successful"
- But no message in server logs

**Diagnosis:**
```bash
# Check destination configuration
grep -n "DESTINATIONS" app/config.py

# Check listening ports
netstat -tulpn | grep 2575
```

**Solutions:**
1. Align client/server ports
```python
# In mllp_client.py - all to 2575
self.default_hosts = {
    "ADMISSION_SYSTEM": {"host": "localhost", "port": 2575},
    "LAB_SYSTEM": {"host": "localhost", "port": 2575},
    # ...
}
```

2. Restart server with verbose logging
```bash
python app/network/mllp_server.py --verbose
```

#### Problem 4: Interface Closes Unexpectedly
**Symptoms (macOS specific):**
```
objc[12345]: autorelease pool page corrupted
Application terminated unexpectedly
```

**Solutions:**
```bash
# Use stable launcher
python run_app.py

# Or define environment variables
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export MALLOC_NANO_ZONE=0
python app/main.py
```

#### Problem 5: Patient Data Not Saved
**Symptoms:**
- Messages sent successfully
- patients.json file empty or not updated

**Diagnosis:**
```bash
# Check file permissions
ls -la resources/patients.json

# Check disk space
df -h .

# Check error logs
grep -i "error.*patient" logs/hl7_messenger.log
```

**Solutions:**
```bash
# Fix permissions
chmod 666 resources/patients.json

# Create file if it doesn't exist
echo "[]" > resources/patients.json

# Restart with appropriate rights
python app/network/mllp_server.py
```

## 🛠️ Diagnostic Tools

### Automatic Diagnostic Script
```bash
# Create and run diagnostic.py
cat > diagnostic.py << 'EOF'
#!/usr/bin/env python3
"""HL7 Messenger Diagnostic Script"""

import socket
import os
import json
import subprocess

def check_python_version():
    import sys
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 8)

def check_dependencies():
    try:
        import hl7apy
        print(f"✅ hl7apy {hl7apy.__version__}")
        return True
    except ImportError:
        print("❌ hl7apy not installed")
        return False

def check_ports_available():
    ports = [2575, 2576, 2577, 2578, 2579]
    available = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        if result != 0:
            available.append(port)
            print(f"✅ Port {port} available")
        else:
            print(f"❌ Port {port} occupied")
        sock.close()
    return len(available) >= 1

def check_files_structure():
    required_files = [
        'app/main.py',
        'app/network/mllp_server.py', 
        'app/network/mllp_client.py',
        'resources/patients.json',
        'requirements.txt'
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_present = False
    return all_present

def main():
    print("🔍 HL7 MESSENGER DIAGNOSTICS")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies), 
        ("Network Ports", check_ports_available),
        ("File Structure", check_files_structure)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        results.append(check_func())
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 SYSTEM READY - All tests passed!")
        print("💡 You can start the application")
    else:
        print("⚠️ PROBLEMS DETECTED - See errors above")
        print("📚 Consult troubleshooting guide")

if __name__ == "__main__":
    main()
EOF

python diagnostic.py
```

### Real-time Monitoring
```bash
# Monitor logs in real-time
tail -f logs/hl7_messenger.log | grep -E "(ERROR|WARNING|INFO)"

# Monitor network connections
watch -n 2 "netstat -an | grep 2575"

# Monitor HL7 processes
watch -n 5 "ps aux | grep -E '(mllp|hl7)'"
```

## 📊 Administration and Maintenance

### 🗄️ Database Management

#### Automatic Backup
```python
# Backup script (backup_database.py)
import shutil
import datetime
import os

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    # Create backup folder
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup critical files
    files_to_backup = [
        "resources/patients.json",
        "resources/messages.json", 
        "app/config.py",
        "logs/hl7_messenger.log"
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
            print(f"✅ {file} backed up")
    
    print(f"💾 Complete backup in {backup_dir}")

if __name__ == "__main__":
    backup_database()
```

#### Data Cleanup
```python
# Cleanup script (cleanup_database.py)
import json
import datetime
from dateutil import parser

def cleanup_old_messages(days_to_keep=30):
    """Remove messages older than X days"""
    
    with open("resources/messages.json", "r") as f:
        messages = json.load(f)
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
    
    filtered_messages = []
    for msg in messages:
        msg_date = parser.parse(msg.get("timestamp", ""))
        if msg_date > cutoff_date:
            filtered_messages.append(msg)
    
    print(f"🗑️ Removing {len(messages) - len(filtered_messages)} old messages")
    
    with open("resources/messages.json", "w") as f:
        json.dump(filtered_messages, f, indent=2)

def archive_old_patients():
    """Archive inactive patients"""
    
    with open("resources/patients.json", "r") as f:
        patients = json.load(f)
    
    # Archive logic based on last activity
    active_patients = []
    archived_patients = []
    
    for patient in patients:
        last_activity = patient.get("metadata", {}).get("last_updated", "")
        # Implementation of archive logic
        active_patients.append(patient)
    
    print(f"📦 {len(archived_patients)} patients archived")
```

### 📈 Reports and Statistics

#### Report Generation
```python
# Report script (generate_report.py)
import json
import datetime
from collections import Counter

def generate_daily_report():
    """Generate daily activity report"""
    
    today = datetime.date.today().strftime("%Y%m%d")
    
    # Load today's messages
    with open("resources/messages.json", "r") as f:
        messages = json.load(f)
    
    daily_messages = [
        msg for msg in messages 
        if msg.get("timestamp", "").startswith(today)
    ]
    
    # Statistics
    stats = {
        "total_messages": len(daily_messages),
        "types_distribution": Counter(msg.get("type", "") for msg in daily_messages),
        "departments": Counter(msg.get("source", "") for msg in daily_messages),
        "success_rate": len([m for m in daily_messages if m.get("status") == "SUCCESS"]) / len(daily_messages) * 100 if daily_messages else 0
    }
    
    # Generate HTML report
    report_html = f"""
    <html>
    <head><title>HL7 Report - {today}</title></head>
    <body>
        <h1>📊 HL7 Activity Report - {today}</h1>
        <h2>General Statistics</h2>
        <ul>
            <li>Total messages: {stats['total_messages']}</li>
            <li>Success rate: {stats['success_rate']:.1f}%</li>
        </ul>
        
        <h2>Distribution by Type</h2>
        <ul>
        {"".join(f"<li>{type_}: {count}</li>" for type_, count in stats['types_distribution'].items())}
        </ul>
        
        <h2>Activity by Department</h2>
        <ul>
        {"".join(f"<li>{dept}: {count}</li>" for dept, count in stats['departments'].items())}
        </ul>
    </body>
    </html>
    """
    
    with open(f"reports/report_{today}.html", "w") as f:
        f.write(report_html)
    
    print(f"📋 Report generated: reports/report_{today}.html")

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    generate_daily_report()
```

### 🔒 Security and Audit

#### Connection Audit
```python
# Security audit script (security_audit.py)
import re
import datetime
from collections import defaultdict

def analyze_security_logs():
    """Analyze security logs"""
    
    failed_connections = defaultdict(int)
    successful_connections = defaultdict(int)
    
    with open("logs/hl7_messenger.log", "r") as f:
        for line in f:
            # Detect failed connection attempts
            if "Connection refused" in line or "Authentication failed" in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    failed_connections[ip_match.group(1)] += 1
            
            # Detect successful connections
            if "Connection established" in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    successful_connections[ip_match.group(1)] += 1
    
    # Detect suspicious attempts (>10 failures)
    suspicious_ips = {ip: count for ip, count in failed_connections.items() if count > 10}
    
    if suspicious_ips:
        print("🚨 SUSPICIOUS ACTIVITY DETECTED:")
        for ip, count in suspicious_ips.items():
            print(f"   IP {ip}: {count} failed attempts")
    else:
        print("✅ No suspicious activity detected")
    
    print(f"\n📊 Connection statistics:")
    print(f"   Successful connections: {sum(successful_connections.values())}")
    print(f"   Failed attempts: {sum(failed_connections.values())}")

if __name__ == "__main__":
    analyze_security_logs()
```

## 🎯 Advanced Usage

### 🔄 Integration with Other Systems

#### REST API for External Integration
```python
# API extension (api_extension.py)
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/patient', methods=['POST'])
def create_patient_via_api():
    """Create patient via REST API"""
    
    patient_data = request.json
    
    # Data validation
    required_fields = ['id', 'last_name', 'first_name']
    for field in required_fields:
        if field not in patient_data:
            return jsonify({"error": f"Field {field} is required"}), 400
    
    # Integration with HL7 system
    from app.hl7_engine.builder import HL7MessageBuilder
    from app.network.mllp_client import MLLPClient
    
    builder = HL7MessageBuilder()
    client = MLLPClient()
    
    # Generate ADT^A01 message  
    message, control_id = builder.create_adt_a01(patient_data)
    
    # Send via MLLP
    success, response = client.send_message(message, "ADMISSION_SYSTEM")
    
    if success:
        return jsonify({
            "status": "success",
            "control_id": control_id,
            "message": "Patient created successfully"
        }), 201
    else:
        return jsonify({
            "status": "error", 
            "message": response
        }), 500

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Retrieve message history"""
    
    with open("resources/messages.json", "r") as f:
        messages = json.load(f)
    
    # Optional filtering
    patient_id = request.args.get('patient_id')
    message_type = request.args.get('type')
    
    if patient_id:
        messages = [m for m in messages if m.get('patient_id') == patient_id]
    
    if message_type:
        messages = [m for m in messages if m.get('type') == message_type]
    
    return jsonify({
        "total": len(messages),
        "messages": messages
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### External Database Connection
```python
# Database extension (database_extension.py)
import sqlite3
import mysql.connector
from contextlib import contextmanager

class DatabaseConnector:
    """Connector for external databases"""
    
    def __init__(self, db_type="sqlite", **kwargs):
        self.db_type = db_type
        self.connection_params = kwargs
    
    @contextmanager
    def get_connection(self):
        """Context manager for DB connections"""
        
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.connection_params.get('database', 'hl7.db'))
        elif self.db_type == "mysql":
            conn = mysql.connector.connect(**self.connection_params)
        else:
            raise ValueError(f"Unsupported DB type: {self.db_type}")
        
        try:
            yield conn
        finally:
            conn.close()
    
    def sync_patients_to_external_db(self):
        """Sync patients to external DB"""
        
        # Load patients from JSON
        with open("resources/patients.json", "r") as f:
            patients = json.load(f)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create table if necessary
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id VARCHAR(50) PRIMARY KEY,
                    last_name VARCHAR(100),
                    first_name VARCHAR(100),
                    birth_date VARCHAR(10),
                    gender CHAR(1),
                    ward VARCHAR(50),
                    room VARCHAR(20),
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert patients
            for patient in patients:
                cursor.execute("""
                    INSERT OR REPLACE INTO patients 
                    (id, last_name, first_name, birth_date, gender, ward, room)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient.get('id'),
                    patient.get('personal_info', {}).get('last_name'),
                    patient.get('personal_info', {}).get('first_name'),
                    patient.get('personal_info', {}).get('birth_date'),
                    patient.get('personal_info', {}).get('gender'),
                    patient.get('hospital_info', {}).get('ward'),
                    patient.get('hospital_info', {}).get('room')
                ))
            
            conn.commit()
            print(f"✅ {len(patients)} patients synced to external DB")

# Usage example
if __name__ == "__main__":
    # Local SQLite
    db_sqlite = DatabaseConnector("sqlite", database="hl7_patients.db")
    db_sqlite.sync_patients_to_external_db()
```

### 📱 Mobile and Web Extensions

#### Simple Web Interface
```html
<!-- Web extension (web_interface.html) -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HL7 Messenger - Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .status { margin-top: 10px; padding: 10px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 HL7 Messenger - Web Interface</h1>
        
        <form id="patientForm">
            <h2>📋 New Patient</h2>
            
            <div class="form-group">
                <label for="patientId">🆔 Patient ID *</label>
                <input type="text" id="patientId" name="patientId" required>
            </div>
            
            <div class="form-group">
                <label for="lastName">👤 Last Name *</label>
                <input type="text" id="lastName" name="lastName" required>
            </div>
            
            <div class="form-group">
                <label for="firstName">👤 First Name *</label>
                <input type="text" id="firstName" name="firstName" required>
            </div>
            
            <div class="form-group">
                <label for="birthDate">📅 Birth Date</label>
                <input type="date" id="birthDate" name="birthDate">
            </div>
            
            <div class="form-group">
                <label for="gender">⚧ Gender</label>
                <select id="gender" name="gender">
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="O">Other</option>
                    <option value="U">Unknown</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="ward">🏢 Ward</label>
                <input type="text" id="ward" name="ward">
            </div>
            
            <div class="form-group">
                <label for="room">🛏️ Room</label>
                <input type="text" id="room" name="room">
            </div>
            
            <button type="submit">🚀 Register Patient</button>
        </form>
        
        <div id="status" class="status" style="display: none;"></div>
        
        <h2>📊 Recent Patients</h2>
        <div id="patientsList">
            <p>Loading...</p>
        </div>
    </div>

    <script>
        // JavaScript for API interaction
        document.getElementById('patientForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const patientData = Object.fromEntries(formData.entries());
            
            // Convert date to HL7 format (YYYYMMDD)
            if (patientData.birthDate) {
                patientData.birth_date = patientData.birthDate.replace(/-/g, '');
                delete patientData.birthDate;
            }
            
            try {
                const response = await fetch('/api/patient', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(patientData)
                });
                
                const result = await response.json();
                const statusDiv = document.getElementById('status');
                
                if (response.ok) {
                    statusDiv.className = 'status success';
                    statusDiv.textContent = '✅ Patient registered successfully!';
                    statusDiv.style.display = 'block';
                    e.target.reset();
                    loadPatients(); // Reload list
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = '❌ Error: ' + result.message;
                    statusDiv.style.display = 'block';
                }
            } catch (error) {
                const statusDiv = document.getElementById('status');
                statusDiv.className = 'status error';
                statusDiv.textContent = '❌ Connection error: ' + error.message;
                statusDiv.style.display = 'block';
            }
        });
        
        async function loadPatients() {
            try {
                const response = await fetch('/api/patients');
                const patients = await response.json();
                
                const patientsDiv = document.getElementById('patientsList');
                if (patients.length === 0) {
                    patientsDiv.innerHTML = '<p>No patients registered</p>';
                } else {
                    patientsDiv.innerHTML = patients.map(patient => `
                        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 4px;">
                            <strong>${patient.id}</strong> - ${patient.last_name} ${patient.first_name}
                            <br><small>Ward: ${patient.ward || 'Not specified'} | Room: ${patient.room || 'Not specified'}</small>
                        </div>
                    `).join('');
                }
            } catch (error) {
                document.getElementById('patientsList').innerHTML = '<p>Error loading patients</p>';
            }
        }
        
        // Load patients on startup
        loadPatients();
    </script>
</body>
</html>
```

## 📚 Resources and References

### 📖 HL7 Documentation

#### HL7 v2.5 Standards
- **HL7 International**: Official HL7 site
- **HL7 v2.5 Standard**: Complete specifications
- **MLLP Protocol**: MLLP protocol RFC

#### Implementation Guides
- **HL7apy Documentation**: Python library documentation
- **ADT Messages**: Admission message structure
- **ORU Messages**: Results message structure
- **ORM Messages**: Order message structure

### 🛠️ Technical Resources

#### Development Tools
```bash
# Useful HL7 tools
pip install hl7apy          # HL7 Python library
pip install python-hl7     # Alternative HL7
pip install hl7-fhir       # FHIR support (future)

# Testing tools
pip install pytest         # Testing framework
pip install mock          # Mocking for tests
pip install coverage      # Test coverage
```

#### HL7 Debug Tools
- **HL7 Inspector**: HL7 message analyzer
- **Mirth Connect**: HL7 integration platform
- **HAPI Test Panel**: HL7 message tester

### 🎓 Training and Certification

#### Learning Resources
- **HL7 University**: Official HL7 training
- **Coursera HL7**: Online courses
- **edX Health Informatics**: Medical informatics

#### Available Certifications
- **HL7 Associate**: Basic certification
- **HL7 Professional**: Advanced certification
- **HL7 Expert**: Expert certification

---

## 📚 Conclusion and Support

You now have the complete user guide for HL7 Messenger, a professional-level hospital messaging solution. This system allows you to:

✅ Manage communication between all hospital departments  
✅ Send and receive standardized HL7 messages  
✅ Store and consult complete exchange history  
✅ Diagnose and resolve technical problems  
✅ Extend and customize the system according to your needs  

### 📞 Support and Assistance

#### Project Contacts
- **👩‍💻 Development Team**: Anouchka, Christelle, Roméo, Calixta
- **🏫 Institution**: Université Libre de Bruxelles (ULB)
- **📧 Main Contact**: ngueanouchka@gmail.com or jeannette.ngue@ulb.be
- **🌐 GitHub Repository**: https://github.com/nouchka9/projet_infoh400

#### Support Resources
- **📖 Technical Documentation**: docs/ folder
- **🐛 Bug Reports**: GitHub Issues
- **💬 Discussions**: Use GitHub discussions
- **📚 Advanced Tutorials**: Project wiki

### 🏆 INFO-H-400 Academic Project

This user guide is an integral part of the project developed as part of the INFO-H-400 "Medical Information Systems" course at ULB.

#### Achieved Learning Objectives
✅ **Complete mastery of HL7 v2.5 standard**  
✅ **Practical implementation of medical protocols**  
✅ **Enterprise-level software architecture**  
✅ **Professional documentation and user guide**  
✅ **Collaborative work with role distribution**  

#### Developed Skills
- **Advanced Programming**: Python, modular architecture
- **Medical Protocols**: HL7, MLLP, international standards
- **User Interface**: Tkinter, ergonomics, UX/UI
- **Network Communication**: TCP/IP, threading, error handling
- **Data Management**: JSON, persistence, history
- **Technical Documentation**: Guides, specifications, support

---

## 📋 Feature Summary

### 🏥 Departmental Modules
| Department | Messages | Key Features |
|------------|----------|--------------|
| 🏥 Admission | ADT^A01-A08 | Patient registration, transfers, discharges |
| 🔬 Laboratory | ORU^R01 | Analysis results, LOINC codes, anomalies |
| 📡 Radiology | ORM^O01, ORU^R01 | Exam orders, reports |
| 💊 Pharmacy | ORM^O01 | Prescriptions, dosages, interactions |

### 🌐 Network Communication
- **MLLP Protocol**: Reliable HL7 message transport
- **Multi-threading**: Simultaneous multiple client management
- **Automatic ACKs**: Message reception confirmation
- **Error Handling**: Diagnosis and automatic recovery

### 💾 Data Management
- **Patient Database**: JSON storage with complete metadata
- **Message History**: Complete exchange traceability
- **Automatic Backup**: Protection against data loss
- **Multiple Export**: CSV, PDF, JSON for analysis

### 🔧 Administration
- **Real-time Monitoring**: Connection and message surveillance
- **Detailed Logs**: Advanced diagnosis and debugging
- **Maintenance Scripts**: Backup, cleanup, reports
- **Flexible Configuration**: Adaptation to specific needs

---

## Next Steps

### To Start Immediately
📥 **Install**: `pip install -r requirements.txt`  
🚀 **Start**: `python app/network/mllp_server.py`  
🔗 **Connect**: anouchka / libre → ADMISSION  
📨 **Test**: Send your first ADT^A01 message  
✅ **Verify**: Check logs and history  

### To Go Further
📚 **Explore** laboratory, radiology, pharmacy modules  
🔧 **Configure** advanced parameters according to your needs  
📊 **Analyze** data with reporting tools  
🌐 **Integrate** with your existing systems via API  
📈 **Extend** features according to your specific needs  

### Recommended Future Developments
🗄️ **Relational Database**: PostgreSQL or MySQL for large volumes  
🌐 **Modern Web Interface**: React or Vue.js for mobility  
🔐 **Advanced Authentication**: LDAP, Active Directory, OAuth2  
📊 **Advanced Analytics**: Interactive dashboards  
🔄 **HL7 FHIR Support**: Next-generation standards  
🐳 **Containerization**: Docker for simplified deployment  

---

## 🏅 Special Thanks

### To the Development Team
- **Anouchka Ngue** : Server architecture and technical leadership
- **Christelle** : Network communication and MLLP protocols
- **Roméo** : User interface and user experience
- **Calixta** : Data management and documentation

### To Academic Supervision
- **ULB Professors**: INFO-H-400 project supervision
- **Université Libre de Bruxelles**: Academic framework of excellence
- **HL7 Community**: Standards and technical specifications

### To Open Source Projects
- **Python Foundation**: Language and ecosystem
- **HL7apy Team**: Quality HL7 library
- **Tkinter Community**: Native graphical interface
- **GitHub**: Collaboration platform

---

## ✅ Final Summary

✅ **Complete hospital messaging solution**  
✅ **Respected standards**: HL7 v2.5 and MLLP  
✅ **Robust architecture** with error handling  
✅ **Intuitive interface** for non-technical users  
✅ **Complete professional documentation**  
✅ **Exhaustive testing and validation**  

###  Potential Impact

This project could serve as a foundation for:
- HL7 training in other universities
- Hospital prototypes for healthcare sector SMEs
- Development tools for HL7 integrators
- Technical references for medical informatics students

---

** HL7 Messenger v1.0 - Complete User Guide**  
*Developed with passion by the INFOH400 team*  
*Université Libre de Bruxelles - May 2025*  

** Need help? Contact us via GitHub or email!**  
** Feel free to contribute to the project and help it evolve!**  

*End of user guide - Thank you for choosing HL7 Messenger! ✨*  
*© 2025 - INFOH400 Team - Université Libre de Bruxelles*  
*All rights reserved - Academic project for educational purposes*
