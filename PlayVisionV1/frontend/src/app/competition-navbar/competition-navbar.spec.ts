import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompetitionNavbar } from './competition-navbar';

describe('CompetitionNavbar', () => {
  let component: CompetitionNavbar;
  let fixture: ComponentFixture<CompetitionNavbar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CompetitionNavbar]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CompetitionNavbar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
