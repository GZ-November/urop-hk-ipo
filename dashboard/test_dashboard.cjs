/* Execute the production dashboard script against a minimal DOM test harness.
   Checks data calculations and event handlers; this is not a layout browser. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(require('node:path').join(__dirname,'index.html'),'utf8');
const payload=JSON.parse(html.match(/<script id="ipo-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
class Element{constructor(id){this.id=id;this.value='';this.innerHTML='';this.textContent='';this.hidden=false;this.handlers={};this.dataset={};this.attributes={};}insertAdjacentHTML(_,s){this.innerHTML+=s;}addEventListener(type,f){this.handlers[type]=f;}setAttribute(k,v){this.attributes[k]=v;}showModal(){this.open=true;}close(){this.open=false;}focus(){}click(){this.handlers.click?.({});}}
const elements=new Map();const get=id=>{if(!elements.has(id))elements.set(id,new Element(id));return elements.get(id);};
get('ipo-data').textContent=JSON.stringify(payload);get('dataset').value='2026';get('sort').value='date-desc';get('coverage-sort').value='schema';
const tabs=['overview','explorer','coverage'].map(t=>{const e=get('tab-'+t);e.dataset.tab=t;return e;});
const context=vm.createContext({document:{getElementById:get,querySelectorAll:()=>tabs,createElement:()=>new Element('download-link')},Blob,URL,setTimeout,console});
vm.runInContext(scripts.join('\n'),context);
const run=code=>vm.runInContext(code,context);
assert.match(get('stats').innerHTML,/>113</);assert.match(get('scope').textContent,/113 of 113/);
const expectedIR=payload.rows.filter(r=>r['Date of Listing (dd/mm/yy)'].startsWith('2026-')).map(r=>r['First-day return / Underpricing (%)']).filter(v=>typeof v==='number').sort((a,b)=>a-b);
assert.equal(run('median(nums(scoped(),K.ir))'),expectedIR[Math.floor(expectedIR.length/2)]);
get('quarter').value='2026Q3';get('quarter').handlers.change();assert.equal(run('scoped().length'),30);assert.match(get('stats').innerHTML,/>30</);
get('route').value='A+H (19A)';get('route').handlers.change();assert.equal(run('scoped().length'),13);
assert.match(get('field-count').textContent,/202 of 202 fields · 13 issuers/);
get('reset').click();assert.equal(run('scoped().length'),113);
tabs[1].click();assert.equal(get('explorer').hidden,false);assert.equal(get('overview').hidden,true);
get('search').value='6872';get('search').handlers.input();assert.equal(run('filtered.length'),1);assert.match(get('issuers').innerHTML,/6872.HK/);
run('showDetail(filtered[0][K.code],filtered[0][K.date])');assert.equal(get('detail').open,true);assert.equal(get('detail-title').textContent,run('selected[K.name]'));
get('detail-search').value='cornerstone';get('detail-search').handlers.input();assert.match(get('detail-table').innerHTML,/Final cornerstone allocation/);assert.doesNotMatch(get('detail-table').innerHTML,/total assets in year-3/);get('close-detail').click();assert.equal(get('detail').open,false);
get('search').value='';get('search').handlers.input();get('next').click();assert.match(get('page-info').textContent,/Showing 26–50/);get('prev').click();assert.match(get('page-info').textContent,/Showing 1–25/);
get('dataset').value='2025';get('dataset').handlers.change();assert.equal(run('filtered.length'),42);assert.equal(run('scoped().length'),113);assert.match(get('explorer-note').textContent,/Q1–Q2 only/);
get('dataset').value='all';get('dataset').handlers.change();assert.equal(run('filtered.length'),155);
get('search').value='no-such-issuer-xyz';get('search').handlers.input();assert.match(get('issuers').innerHTML,/No observations/);assert.equal(get('next').disabled,true);
get('search').value='';get('dataset').value='2026';get('sort').value='return-desc';get('sort').handlers.change();assert.ok(run('filtered[0][K.ir]>=filtered[1][K.ir]'));
assert.equal(run('pct(null)'),'—');assert.equal(run('pct(0)'),'0%');assert.equal(run('pct(.1)'),'10%');assert.equal(run('median([])'),null);
assert.equal(run('csvCell("=SUM(A1)")'),'"\'=SUM(A1)"');assert.equal(run('csvCell(-.1)'),'"-0.1"');assert.equal(run('csvCell(null)'),'""');
assert.ok(run('csvText(filtered).startsWith("\\uFEFF")'));assert.match(run('esc("<script>")'),/&lt;script&gt;/);
get('field-search').value='cornerstone';get('field-search').handlers.input();assert.match(get('coverage-table').innerHTML,/Final cornerstone allocation/);
get('field-search').value='xyz-no-field';get('field-search').handlers.input();assert.match(get('coverage-table').innerHTML,/No observations/);
get('quarter').value='2026Q3';get('route').value='18A biotech';get('quarter').handlers.change();assert.equal(run('scoped().length'),0);assert.match(get('scatter').innerHTML,/No observations/);assert.doesNotMatch(get('stats').innerHTML,/NaN|Infinity/);
console.log('Dashboard JavaScript checks passed: metrics, filters, archive, search, sort, pagination, details, coverage, empty state and CSV.');
