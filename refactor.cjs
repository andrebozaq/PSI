const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const moves = [
  { from: 'src/lib/firebaseConfig.ts', to: 'src/config/firebase.ts' },
  { from: 'src/components/auth/SignInForm.tsx', to: 'src/features/auth/components/SignInForm.tsx' },
  { from: 'src/components/auth/SignUpForm.tsx', to: 'src/features/auth/components/SignUpForm.tsx' },
  { from: 'src/contexts/AuthContext.tsx', to: 'src/features/auth/contexts/AuthContext.tsx' },
  { from: 'src/services/authService.ts', to: 'src/features/auth/services/authService.ts' },
  { from: 'src/pages/AuthPages/SignIn.tsx', to: 'src/features/auth/pages/SignIn.tsx' },
  { from: 'src/pages/AuthPages/SignUp.tsx', to: 'src/features/auth/pages/SignUp.tsx' },
  { from: 'src/pages/AuthPages/ResetPassword.tsx', to: 'src/features/auth/pages/ResetPassword.tsx' },
  { from: 'src/pages/AuthPages/TwoStepVerification.tsx', to: 'src/features/auth/pages/TwoStepVerification.tsx' },
  
  { from: 'src/components/forum/NewPostModal.tsx', to: 'src/features/forum/components/NewPostModal.tsx' },
  { from: 'src/pages/ForumDashboard.tsx', to: 'src/features/forum/pages/ForumDashboard.tsx' },
  { from: 'src/pages/PostDetail.tsx', to: 'src/features/forum/pages/PostDetail.tsx' },
  
  { from: 'src/components/UserProfile/UserMetaCard.tsx', to: 'src/features/profile/components/UserMetaCard.tsx' },
  { from: 'src/pages/UserProfiles.tsx', to: 'src/features/profile/pages/UserProfiles.tsx' },
  { from: 'src/services/userService.ts', to: 'src/features/profile/services/userService.ts' },
  
  { from: 'src/pages/Pressure/DesignSupport.tsx', to: 'src/features/engineering/pages/DesignSupport.tsx' },
  { from: 'src/pages/Pressure/AnalysisDashboard.tsx', to: 'src/features/engineering/pages/AnalysisDashboard.tsx' },
  { from: 'src/pages/SavedProjects.tsx', to: 'src/features/engineering/pages/SavedProjects.tsx' },
  
  { from: 'src/pages/Pressure/components/GeometryCard.tsx', to: 'src/features/engineering/components/GeometryCard.tsx' },
  { from: 'src/pages/Pressure/components/SeismicCard.tsx', to: 'src/features/engineering/components/SeismicCard.tsx' },
  { from: 'src/pages/Pressure/components/SummaryReport.tsx', to: 'src/features/engineering/components/SummaryReport.tsx' },
  { from: 'src/pages/Pressure/components/WindCard.tsx', to: 'src/features/engineering/components/WindCard.tsx' },
  
  // supports
  { from: 'src/pages/Pressure/supports/Anchoring.tsx', to: 'src/features/engineering/supports/Anchoring.tsx' },
  { from: 'src/pages/Pressure/supports/Legs.tsx', to: 'src/features/engineering/supports/Legs.tsx' },
  { from: 'src/pages/Pressure/supports/Lug.tsx', to: 'src/features/engineering/supports/Lug.tsx' },
  { from: 'src/pages/Pressure/supports/RingSupport.tsx', to: 'src/features/engineering/supports/RingSupport.tsx' },
  { from: 'src/pages/Pressure/supports/Saddle.tsx', to: 'src/features/engineering/supports/Saddle.tsx' },
  { from: 'src/pages/Pressure/supports/Skirt.tsx', to: 'src/features/engineering/supports/Skirt.tsx' },
  { from: 'src/pages/Pressure/supports/SupportCommon.tsx', to: 'src/features/engineering/supports/SupportCommon.tsx' },
];

const designCalculations = [
  'AnchorUtils.tsx', 'Constants.tsx', 'DesignEngine.tsx', 'DesignThresholds.ts',
  'EnvironmentalUtils.tsx', 'LegCalc.tsx', 'LegUtils.tsx', 'LugCalc.tsx', 'LugUtils.tsx',
  'PhysicsUtils.tsx', 'RingCalc.tsx', 'RingUtils.tsx', 'SaddleCalc.tsx', 'SaddleUtils.tsx',
  'SkirtCalc.tsx', 'SkirtUtils.tsx'
];
for (const file of designCalculations) {
  moves.push({
    from: `src/pages/Pressure/supports/DesignCalculations/${file}`,
    to: `src/features/engineering/supports/DesignCalculations/${file}`
  });
}

// 1. Rename files on disk using git mv
for (const move of moves) {
  if (fs.existsSync(move.from)) {
    try {
      execSync(`git mv "${move.from}" "${move.to}"`);
      console.log(`Moved: ${move.from} -> ${move.to}`);
    } catch(e) {
      console.log(`Fallback to fs.renameSync for ${move.from}`);
      fs.renameSync(move.from, move.to);
    }
  }
}

// 2. Build a mapping of original absolute path (without extension) -> new absolute path (without extension)
const rootDir = __dirname;
const pathMap = new Map();

for (const move of moves) {
  const oldAbs = path.join(rootDir, move.from);
  const newAbs = path.join(rootDir, move.to);
  // remove extensions to easily match imports like '../../services/authService'
  const oldNoExt = oldAbs.replace(/\.(tsx|ts|jsx|js)$/, '');
  const newNoExt = newAbs.replace(/\.(tsx|ts|jsx|js)$/, '');
  pathMap.set(oldNoExt.replace(/\\/g, '/'), newNoExt.replace(/\\/g, '/'));
}

// helper to get old location if a file was moved
function getOldLocation(newLocation) {
  const normNew = newLocation.replace(/\\/g, '/');
  for (const move of moves) {
    if (path.join(rootDir, move.to).replace(/\\/g, '/') === normNew) {
      return path.join(rootDir, move.from).replace(/\\/g, '/');
    }
  }
  return normNew;
}

// 3. Process all TS/TSX files
function getFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      if (file !== 'node_modules' && file !== '.git') {
        getFiles(filePath, fileList);
      }
    } else if (/\.(ts|tsx)$/.test(filePath)) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

const allFiles = getFiles(path.join(rootDir, 'src'));

let filesChanged = 0;

for (const file of allFiles) {
  let content = fs.readFileSync(file, 'utf8');
  let changed = false;

  // Find all relative imports
  const importRegex = /(?:import|export)\s+.*?\s+from\s+['"](\.[^'"]+)['"]/g;
  const requireRegex = /require\(['"](\.[^'"]+)['"]\)/g;

  function replaceImport(match, p1) {
    // p1 is the relative path, e.g. '../../services/authService'
    // To resolve it, we need to pretend the current file is in its OLD location
    const oldFileLocation = getOldLocation(file);
    const oldDirLocation = path.dirname(oldFileLocation);
    
    // The target's OLD absolute path
    const targetOldAbs = path.resolve(oldDirLocation, p1).replace(/\\/g, '/');
    
    // Check if the target moved
    let targetNewAbs = targetOldAbs; // defaults to old
    if (pathMap.has(targetOldAbs)) {
      targetNewAbs = pathMap.get(targetOldAbs);
    } else {
        // Also check if index was implied, e.g. targetOldAbs/index
        if (pathMap.has(targetOldAbs + '/index')) {
             targetNewAbs = pathMap.get(targetOldAbs + '/index');
        }
    }

    // New relative path from NEW file location to NEW target location
    const currentNewDir = path.dirname(file).replace(/\\/g, '/');
    let newRelative = path.relative(currentNewDir, targetNewAbs).replace(/\\/g, '/');
    
    if (!newRelative.startsWith('.')) {
      newRelative = './' + newRelative;
    }

    if (p1 !== newRelative) {
      changed = true;
      return match.replace(p1, newRelative);
    }
    
    return match;
  }

  content = content.replace(importRegex, replaceImport);
  content = content.replace(requireRegex, replaceImport);

  // Note: we also have cases where a file DIDN'T move, but imports a file that DID move.
  // The logic `getOldLocation(file)` handles this gracefully because if the file didn't move,
  // oldFileLocation == current location. Then `targetOldAbs` is checked in pathMap, and we 
  // compute `newRelative` based on the target's new location.

  if (changed) {
    fs.writeFileSync(file, content, 'utf8');
    filesChanged++;
  }
}

console.log(`Refactor complete. Updated imports in ${filesChanged} files.`);
